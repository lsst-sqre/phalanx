#!/bin/bash
# server-wrapper.sh around the pinned image's real clickhouse-server, run under
# Apptainer: clean shutdown on SIGTERM and SIGINT, a crash, a restart on the
# same data, and a guard refusal. The server gets the chart's own config.d and
# users.d (from tests/golden, which render_test.py ties to the render), except
# that it listens on 127.0.0.1 only and on free, non-default ports, with an
# empty data directory under WORK.
#
# Run by run-tests.sh. Inputs: IMAGE (docker:// reference or SIF), WORK (empty
# scratch directory), SCRIPTS (directory holding the two scripts).

set -uo pipefail

: "${IMAGE:?}" "${WORK:?}" "${SCRIPTS:?}"
HERE="$(cd "$(dirname "$0")" && pwd)"
pass=0
fail=0
ok() { pass=$((pass + 1)); echo "ok   $*"; }
bad() { fail=$((fail + 1)); echo "FAIL $*"; }
expect() {
    local d="$1"; shift
    if "$@"; then ok "$d"; else bad "$d"; fi
}

free_port() {
    python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])'
}
HTTP_PORT=$(free_port)
TCP_PORT=$(free_port)
CLOSED_PORT=$(free_port)
D="$WORK/data"
UF="$WORK/user-files"
mkdir -p "$D" "$UF" "$WORK/config.d" "$WORK/users.d"

# The chart's server configuration, verbatim but for the listen addresses...
python3 - "$HERE/golden/clickhouse-configmap-data.json" "$WORK" <<'EOF'
import json, sys
data = json.load(open(sys.argv[1]))
for key, text in data.items():
    d, name = key.split("-", 1)
    if name == "paths.xml":
        text = text.replace("<listen_host>::</listen_host>\n", "").replace(
            "<listen_host>0.0.0.0</listen_host>", "<listen_host>127.0.0.1</listen_host>")
    open(f"{sys.argv[2]}/{d}/{name}", "w").write(text)
EOF
# ...and the ports.
cat >"$WORK/config.d/zz-test-ports.xml" <<EOF
<clickhouse>
  <http_port>$HTTP_PORT</http_port>
  <tcp_port>$TCP_PORT</tcp_port>
</clickhouse>
EOF
# Throwaway password hashes for users.d's from_env (hashes of random bytes,
# never used to log in), passed only through an env file.
umask 077
{
    for v in ADMIN_SHA256 MPPDB_RO_SHA256 SSP_XMATCH_SHA256; do
        echo "$v=$(head -c 32 /dev/urandom | sha256sum | cut -d' ' -f1)"
    done
    echo "CLICKHOUSE_SKIP_USER_SETUP=1"
    echo "RNF_SIDE=pod"
    echo "RNF_IDENT=test-pod-0"
    echo "RNF_OTHER_SIDE=sdfiana032"
    echo "RNF_OTHER_PING_URL=http://127.0.0.1:$CLOSED_PORT/ping"
    echo "RNF_HEARTBEAT_SECONDS=2"
    echo "RNF_STALE_SECONDS=6"
} >"$WORK/env"
umask 022

URL="http://127.0.0.1:$HTTP_PORT"
q() { curl --noproxy '*' -sf --max-time 30 "$URL/" --data-binary "$1"; }
pinging() { curl --noproxy '*' -sf --max-time 3 -o /dev/null "$URL/ping"; }
owner() { cat "$D/.owner" 2>/dev/null; }
owner_is() {
    case "$(owner)" in "$1 "????-??-??T??:??:??Z) return 0 ;; esac
    echo "     owner line is '$(owner)', wanted '$1 <time>'" >&2
    return 1
}
wait_for() {
    local n="$1"; shift
    while [ "$n" -gt 0 ]; do
        "$@" && return 0
        sleep 1
        n=$((n - 1))
    done
    return 1
}

# start: run the wrapper in the container, as the pod would (clean
# environment, read-only image, the same mount points), with SIGINT and
# SIGTERM at their defaults.
start() {
    perl -e '$SIG{INT} = $SIG{TERM} = "DEFAULT"; exec @ARGV or die' \
        apptainer exec --contain --cleanenv --env-file "$WORK/env" \
        --bind "$D:/var/lib/clickhouse" \
        --bind "$UF:/var/lib/clickhouse-user-files" \
        --bind "$WORK/config.d:/etc/clickhouse-server/config.d" \
        --bind "$WORK/users.d:/etc/clickhouse-server/users.d" \
        --bind "$SCRIPTS:/opt/river-failover" \
        "$IMAGE" /bin/sh /opt/river-failover/server-wrapper.sh \
        >>"$WORK/wrapper.log" 2>&1 &
    apid=$!
}
gone() { ! kill -0 "$apid" 2>/dev/null; }
finish() {
    if wait_for 300 gone; then
        wait "$apid"
        rc=$?
    else
        kill -9 "$apid" 2>/dev/null
        rc=timeout
    fi
}
server_pid() { sed -n 's/^PID: *//p' "$D/status" 2>/dev/null; }

echo "== real clickhouse-server (http $HTTP_PORT, native $TCP_PORT)"

# A. First start on an empty directory; clean shutdown on SIGTERM.
start
expect "A: server answers /ping under the wrapper" wait_for 240 pinging
expect "A: owner line is pod test-pod-0" owner_is "pod test-pod-0"
expect "A: heartbeat written" test -e "$D/.heartbeat-pod"
expect "A: status file written (what the liveness probe reads)" grep -q '^PID:' "$D/status"
for sub in logs tmp format_schemas; do
    expect "A: server created $sub/ itself (the entrypoint's mkdir is not needed)" test -d "$D/$sub"
done
expect "A: server logs to logs/clickhouse-server.log" test -s "$D/logs/clickhouse-server.log"
parent=$(ps -o ppid= -p "$(server_pid)" 2>/dev/null | tr -d ' ')
expect "A: no watchdog: the server's parent is the wrapper's sh ($(ps -o comm= -p "$parent" 2>/dev/null))" \
    test "$(ps -o comm= -p "$parent" 2>/dev/null)" = sh
q "CREATE TABLE default.t (x UInt64) ENGINE = MergeTree ORDER BY x" >/dev/null
q "INSERT INTO default.t SELECT number FROM numbers(1000)" >/dev/null
expect "A: a table can be written" test "$(q 'SELECT count() FROM default.t')" = 1000
kill -TERM "$apid"
finish
expect "A: SIGTERM gives a clean exit (got $rc)" test "$rc" = 0
expect "A: released pod/test-pod-0" owner_is "released pod/test-pod-0"
expect "A: heartbeat removed" test ! -e "$D/.heartbeat-pod"
expect "A: server stopped" sh -c "! curl --noproxy '*' -sf --max-time 3 -o /dev/null $URL/ping"

# B. Restart on the same data; clean shutdown on SIGINT.
start
expect "B: restarts after its own release" wait_for 240 pinging
expect "B: data survived the clean shutdown" test "$(q 'SELECT count() FROM default.t')" = 1000
kill -INT "$apid"
finish
expect "B: SIGINT gives a clean exit (got $rc)" test "$rc" = 0
expect "B: released again" owner_is "released pod/test-pod-0"

# C. The server is killed: the owner line stays, and the same side restarts.
start
wait_for 240 pinging
spid=$(server_pid)
expect "C: found the server's PID ($spid)" test -n "$spid"
[ -n "$spid" ] && kill -KILL "$spid"
finish
expect "C: killed server gives 137 (got $rc)" test "$rc" = 137
expect "C: owner line kept as pod test-pod-0" owner_is "pod test-pod-0"
expect "C: heartbeat removed" test ! -e "$D/.heartbeat-pod"
start
expect "C: same side restarts on its own owner line" wait_for 240 pinging
expect "C: data intact after the crash" test "$(q 'SELECT count() FROM default.t')" = 1000
kill -TERM "$apid"
finish
expect "C: clean exit after the restart (got $rc)" test "$rc" = 0

# D. The other side owns the directory: the server never starts.
echo "sdfiana032 4242 2026-10-05T00:00:00Z" >"$D/.owner"
start
finish
expect "D: guard refusal exits 1 (got $rc)" test "$rc" = 1
expect "D: the server never started" sh -c "! curl --noproxy '*' -sf --max-time 3 -o /dev/null $URL/ping"
expect "D: no heartbeat" test ! -e "$D/.heartbeat-pod"
expect "D: owner line untouched" owner_is "sdfiana032 4242"
expect "D: refusal names the rule" grep -q 'rule 1 (owner)' "$WORK/wrapper.log"

if [ "$fail" != 0 ]; then
    echo "--- wrapper and server console output"
    cat "$WORK/wrapper.log"
fi
echo
echo "real_server_test: $pass passed, $fail failed"
[ "$fail" = 0 ]
