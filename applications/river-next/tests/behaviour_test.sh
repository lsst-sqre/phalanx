#!/bin/sh
# Behaviour test of owner-guard.sh and server-wrapper.sh: every start rule,
# --check-only, and the wrapper's exit paths, against a throwaway data
# directory, fake /ping URLs and a stub clickhouse-server.
#
# Run by run-tests.sh, normally inside the pinned ClickHouse image (so the
# scripts meet the same dash and wget they will in production). Inputs:
#   SCRIPTS      directory holding owner-guard.sh and server-wrapper.sh
#   STUB_DIR     directory holding the stub clickhouse-server
#   WORK         empty scratch directory
#   PING_OK_URL      answers 200 "Ok."
#   PING_ERR_URL     answers with an HTTP error (404)
#   PING_CLOSED_URL  nothing listening
#   PROXY_URL        an HTTP server that would answer any proxied request

set -u

: "${SCRIPTS:?}" "${STUB_DIR:?}" "${WORK:?}"
: "${PING_OK_URL:?}" "${PING_ERR_URL:?}" "${PING_CLOSED_URL:?}" "${PROXY_URL:?}"

GUARD="$SCRIPTS/owner-guard.sh"
WRAPPER="$SCRIPTS/server-wrapper.sh"
pass=0
fail=0

ok() { pass=$((pass + 1)); echo "ok   $*"; }
bad() { fail=$((fail + 1)); echo "FAIL $*"; }
expect() {
    # expect <description> <command...>: the command must succeed.
    _d="$1"; shift
    if "$@"; then ok "$_d"; else bad "$_d"; fi
}

D="$WORK/data"
reset() {
    rm -rf "$D"
    mkdir -p "$D"
}

# Defaults for the pod side; individual cases override.
set_pod() {
    RNF_SIDE=pod RNF_OTHER_SIDE=sdfiana032 RNF_IDENT=river-next-clickhouse-0
    RNF_OTHER_PING_URL="$PING_CLOSED_URL" RNF_DATA_DIR="$D"
    RNF_STALE_SECONDS=3 RNF_HEARTBEAT_SECONDS=1
    export RNF_SIDE RNF_OTHER_SIDE RNF_IDENT RNF_OTHER_PING_URL RNF_DATA_DIR \
        RNF_STALE_SECONDS RNF_HEARTBEAT_SECONDS
    unset RNF_EXPECT_HOST
}
set_ana() {
    set_pod
    RNF_SIDE=sdfiana032 RNF_OTHER_SIDE=pod
    unset RNF_IDENT
}

# guard [args]: run the guard, capturing status, stdout and stderr.
guard() {
    sh "$GUARD" "$@" >"$WORK/out" 2>"$WORK/err"
    rc=$?
}

owner() { cat "$D/.owner" 2>/dev/null; }
owner_is() {
    # owner_is <expected prefix>: the owner line starts with it, followed by
    # a UTC ISO time.
    case "$(owner)" in
        "$1 "????-??-??T??:??:??Z) return 0 ;;
    esac
    echo "     owner line is: '$(owner)', wanted '$1 <time>'" >&2
    return 1
}
no_tmp() { [ -z "$(find "$D" -name '*.tmp.*' 2>/dev/null)" ]; }
refused() {
    # refused <rule text>: exit 1, exactly one line on stderr naming the rule,
    # nothing on stdout.
    if [ "$rc" = 1 ] && [ "$(wc -l <"$WORK/err")" = 1 ] \
        && grep -q "$1" "$WORK/err" && [ ! -s "$WORK/out" ]; then
        return 0
    fi
    echo "     rc=$rc stderr: $(cat "$WORK/err") stdout: $(cat "$WORK/out")" >&2
    return 1
}
passed() {
    if [ "$rc" = 0 ]; then return 0; fi
    echo "     rc=$rc stderr: $(cat "$WORK/err")" >&2
    return 1
}
fresh_hb() { date -u +%Y-%m-%dT%H:%M:%SZ >"$D/.heartbeat-$1"; }
stale_hb() { fresh_hb "$1"; touch -d '-10 seconds' "$D/.heartbeat-$1"; }

echo "== owner-guard.sh ($(readlink -f /bin/sh))"

# Rule 1: owner.
set_pod; reset; guard
expect "rule 1: missing owner file means pod; pod may start" passed
expect "claim: owner line is 'pod <ident> <time>'" owner_is "pod river-next-clickhouse-0"
expect "claim: no temp file left behind" no_tmp

set_pod; reset; echo "released sdfiana032/1234 2026-10-05T00:00:00Z" >"$D/.owner"; guard
expect "rule 1: released (by the other side) lets pod start" passed
expect "rule 1: ... and pod claims it" owner_is "pod river-next-clickhouse-0"

set_pod; reset; echo "pod river-next-clickhouse-0 2026-10-05T00:00:00Z" >"$D/.owner"; guard
expect "rule 1: owner names this side; may start" passed

set_pod; reset; echo "pod some-other-pod 2026-10-05T00:00:00Z" >"$D/.owner"; guard
expect "rule 1: owner names this side with another ident; may start" passed

set_pod; reset; echo "sdfiana032 4242 2026-10-05T00:00:00Z" >"$D/.owner"; guard
expect "rule 1: owner names the other side; pod refuses" refused "rule 1 (owner)"
expect "rule 1: refusal leaves the owner line alone" owner_is "sdfiana032 4242"

set_pod; reset; echo "garbage" >"$D/.owner"; guard
expect "rule 1: unknown owner state refuses" refused "rule 1 (owner)"

set_pod; reset; : >"$D/.owner"; guard
expect "rule 1: empty owner file refuses" refused "rule 1 (owner)"

set_ana; reset; guard
expect "rule 1: missing owner file means pod; sdfiana032 refuses" refused "rule 1 (owner)"

set_ana; reset; echo "released pod/river-next-clickhouse-0 2026-10-05T00:00:00Z" >"$D/.owner"; guard
expect "rule 1: released by pod lets sdfiana032 start" passed
case "$(owner)" in
    "sdfiana032 "[0-9]*" "*) ok "claim: unset RNF_IDENT means a PID ident" ;;
    *) bad "claim: unset RNF_IDENT means a PID ident (owner: $(owner))" ;;
esac

# Rule 2: the other side's heartbeat.
set_pod; reset; fresh_hb sdfiana032; guard
expect "rule 2: fresh heartbeat of the other side refuses" refused "rule 2 (heartbeat)"
expect "rule 2: refusal writes no owner file" test ! -e "$D/.owner"

set_pod; reset; stale_hb sdfiana032; guard
expect "rule 2: stale heartbeat of the other side passes" passed

set_pod; reset; fresh_hb pod; guard
expect "rule 2: this side's own fresh heartbeat is ignored" passed

set_pod; reset; fresh_hb sdfiana032; touch -d '+60 seconds' "$D/.heartbeat-sdfiana032"; guard
expect "rule 2: a heartbeat from the future (clock skew) refuses" refused "rule 2 (heartbeat)"

set_ana; reset; echo "released pod/x 2026-10-05T00:00:00Z" >"$D/.owner"; fresh_hb pod; guard
expect "rule 2: sdfiana032 refuses on pod's fresh heartbeat" refused "rule 2 (heartbeat)"

# Rule 3: the other side's /ping.
set_pod; reset; RNF_OTHER_PING_URL="$PING_OK_URL"; guard
expect "rule 3: other side answering /ping refuses" refused "rule 3 (ping)"
expect "rule 3: refusal writes no owner file" test ! -e "$D/.owner"

set_pod; reset; RNF_OTHER_PING_URL="$PING_ERR_URL"; guard
expect "rule 3: a server answering with an HTTP error refuses" refused "rule 3 (ping)"

set_pod; reset; RNF_OTHER_PING_URL="$PING_CLOSED_URL"; guard
expect "rule 3: nothing listening passes" passed

prc=0
http_proxy="$PROXY_URL" no_proxy="" wget -q -t 1 -T 3 -O /dev/null "$PING_CLOSED_URL" || prc=$?
expect "rule 3 control: through the proxy, the closed URL does answer (wget $prc)" \
    test "$prc" = 0 -o "$prc" = 8
set_pod; reset
http_proxy="$PROXY_URL" HTTP_PROXY="$PROXY_URL" no_proxy="" NO_PROXY="" \
    sh "$GUARD" >"$WORK/out" 2>"$WORK/err"
rc=$?
expect "rule 3: the ping bypasses http_proxy (a proxy would have answered)" passed

set_pod; reset; RNF_OTHER_PING_URL="http://192.0.2.1:8123/ping"
t0=$(date +%s); guard; t1=$(date +%s)
expect "rule 3: unroutable address passes" passed
expect "rule 3: ... within the 3 s timeout (took $((t1 - t0)) s)" test $((t1 - t0)) -le 5

# Rule 4: host.
set_ana; reset; echo "released pod/x 2026-10-05T00:00:00Z" >"$D/.owner"
RNF_EXPECT_HOST="$(hostname -s)"; export RNF_EXPECT_HOST; guard
expect "rule 4: matching host passes" passed
set_ana; reset; echo "released pod/x 2026-10-05T00:00:00Z" >"$D/.owner"
RNF_EXPECT_HOST="not-$(hostname -s)"; export RNF_EXPECT_HOST; guard
expect "rule 4: any other host refuses" refused "rule 4 (host)"
unset RNF_EXPECT_HOST

# All rules together: the failing one is the one reported.
set_pod; reset; echo "released sdfiana032/1 2026-10-05T00:00:00Z" >"$D/.owner"
stale_hb sdfiana032; RNF_OTHER_PING_URL="$PING_OK_URL"; guard
expect "rules 1-2 pass, 3 fails: reports rule 3 only" refused "rule 3 (ping)"

# --check-only.
set_pod; reset; guard --check-only
expect "--check-only: passes" passed
expect "--check-only: writes nothing" test ! -e "$D/.owner"
set_pod; reset; echo "released sdfiana032/1 2026-10-05T00:00:00Z" >"$D/.owner"; guard --check-only
expect "--check-only: leaves a released line alone" owner_is "released sdfiana032/1"
set_pod; reset; fresh_hb sdfiana032; guard --check-only
expect "--check-only: still refuses" refused "rule 2 (heartbeat)"
set_pod; reset; guard --bogus
expect "an unknown argument is an error" test "$rc" = 2

# Configuration errors.
set_pod; reset; unset RNF_SIDE; guard
expect "config: RNF_SIDE unset refuses" refused "config: RNF_SIDE"
set_pod; reset; RNF_OTHER_SIDE=pod; guard
expect "config: same side twice refuses" refused "config:"
set_pod; RNF_DATA_DIR="$WORK/nonexistent"; guard
expect "config: missing data directory refuses" refused "config: data directory"

echo "== server-wrapper.sh"

PATH="$STUB_DIR:$PATH"
export PATH
LOG="$WORK/stub.log"
export STUB_LOG="$LOG"

# start_wrapper <mode> [args]: start the wrapper in the background, with
# SIGINT and SIGTERM at their defaults (a plain `&` would start it with
# SIGINT ignored, which a POSIX shell cannot trap).
start_wrapper() {
    _mode="$1"; shift
    : >"$LOG"
    STUB_MODE="$_mode" perl -e '$SIG{INT} = $SIG{TERM} = "DEFAULT"; exec @ARGV or die' \
        sh "$WRAPPER" "$@" >"$WORK/wout" 2>"$WORK/werr" &
    wpid=$!
}
# wait_for <tenths> <command...>: poll until the command succeeds.
wait_for() {
    _n="$1"; shift
    while [ "$_n" -gt 0 ]; do
        "$@" && return 0
        sleep 0.1
        _n=$((_n - 1))
    done
    return 1
}
started() { grep -q '^started' "$LOG"; }
wrapper_done() { ! kill -0 "$wpid" 2>/dev/null; }
finish() {
    # finish: wait (bounded) for the wrapper and collect its status.
    if wait_for 150 wrapper_done; then
        wait "$wpid"
        wrc=$?
    else
        kill -9 "$wpid" 2>/dev/null
        wrc=timeout
    fi
}
hb_mtime() { stat -c %Y "$D/.heartbeat-$1" 2>/dev/null; }

# Clean shutdown on SIGTERM: released, heartbeat gone, status 0.
set_pod; reset
start_wrapper term0 --extra-arg
expect "wrapper: server started" wait_for 50 started
expect "wrapper: heartbeat written while the server runs" wait_for 30 test -e "$D/.heartbeat-pod"
m1=$(hb_mtime pod); sleep 2.2; m2=$(hb_mtime pod)
expect "wrapper: heartbeat refreshed every RNF_HEARTBEAT_SECONDS ($m1 -> $m2)" test "${m2:-0}" -gt "${m1:-0}"
expect "wrapper: owner line is pod <ident> while running" owner_is "pod river-next-clickhouse-0"
expect "wrapper: the other side's guard refuses while it runs (rule 1)" \
    sh -c 'RNF_SIDE=sdfiana032 RNF_OTHER_SIDE=pod; export RNF_SIDE RNF_OTHER_SIDE; ! sh "$1" --check-only 2>/dev/null' _ "$GUARD"
kill -TERM "$wpid"; finish
expect "wrapper: SIGTERM forwarded to the server" grep -q '^signal TERM' "$LOG"
expect "wrapper: exit 0 on a clean shutdown (got $wrc)" test "$wrc" = 0
expect "wrapper: clean exit writes released pod/<ident>" owner_is "released pod/river-next-clickhouse-0"
expect "wrapper: heartbeat removed" test ! -e "$D/.heartbeat-pod"
expect "wrapper: no temp files left behind" no_tmp
expect "wrapper: server ran with --config-file and the extra arguments" \
    grep -qx 'args=--config-file=/etc/clickhouse-server/config.xml --extra-arg' "$LOG"
expect "wrapper: server ran in the data directory" grep -qx "cwd=$(cd "$D" && pwd -P)" "$LOG"
expect "wrapper: watchdog disabled, as the image entrypoint does" grep -qx 'watchdog=0' "$LOG"
sleep 2
expect "wrapper: heartbeat stays gone after exit" test ! -e "$D/.heartbeat-pod"

# SIGINT is forwarded too.
set_pod; reset
start_wrapper term0
wait_for 50 started
kill -INT "$wpid"; finish
expect "wrapper: SIGINT forwarded to the server" grep -q '^signal INT' "$LOG"
expect "wrapper: exit 0 after SIGINT (got $wrc)" test "$wrc" = 0
expect "wrapper: released after SIGINT" owner_is "released pod/river-next-clickhouse-0"

# Non-zero exit after a signal: owner line kept, heartbeat gone, status passed on.
set_pod; reset
start_wrapper term3
wait_for 50 started
wait_for 30 test -e "$D/.heartbeat-pod"
kill -TERM "$wpid"; finish
expect "wrapper: server's status 3 passed on (got $wrc)" test "$wrc" = 3
expect "wrapper: non-zero exit keeps the owner line" owner_is "pod river-next-clickhouse-0"
expect "wrapper: non-zero exit removes the heartbeat" test ! -e "$D/.heartbeat-pod"
set_pod; guard
expect "wrapper: after a non-zero exit this side may restart" passed

# The server crashing on its own.
set_pod; reset
start_wrapper crash7; finish
expect "wrapper: crash status 7 passed on (got $wrc)" test "$wrc" = 7
expect "wrapper: crash keeps the owner line" owner_is "pod river-next-clickhouse-0"
expect "wrapper: crash removes the heartbeat" test ! -e "$D/.heartbeat-pod"

# The server killed by a signal.
set_pod; reset
start_wrapper kill9; finish
expect "wrapper: server killed by SIGKILL gives 137 (got $wrc)" test "$wrc" = 137
expect "wrapper: ... and keeps the owner line" owner_is "pod river-next-clickhouse-0"

# The server exiting 0 by itself.
set_pod; reset
start_wrapper exit0; finish
expect "wrapper: unprompted clean exit gives 0 (got $wrc)" test "$wrc" = 0
expect "wrapper: ... and releases" owner_is "released pod/river-next-clickhouse-0"

# Guard refusal: the server never starts.
set_pod; reset; echo "sdfiana032 4242 2026-10-05T00:00:00Z" >"$D/.owner"
start_wrapper term0; finish
expect "wrapper: guard refusal exits 1 (got $wrc)" test "$wrc" = 1
expect "wrapper: guard refusal does not start the server" test ! -s "$LOG"
expect "wrapper: guard refusal writes no heartbeat" test ! -e "$D/.heartbeat-pod"
expect "wrapper: guard refusal leaves the owner line" owner_is "sdfiana032 4242"
expect "wrapper: guard refusal is one line naming the rule" \
    sh -c '[ "$(wc -l <"$1")" = 1 ] && grep -q "rule 1 (owner)" "$1"' _ "$WORK/werr"

# The failover side: ident is the wrapper's PID, and it releases with it.
set_ana; reset; echo "released pod/river-next-clickhouse-0 2026-10-05T00:00:00Z" >"$D/.owner"
start_wrapper term0
wait_for 50 started
wait_for 30 test -e "$D/.heartbeat-sdfiana032"
expect "wrapper (sdfiana032): owner line is sdfiana032 <wrapper pid>" owner_is "sdfiana032 $wpid"
expect "wrapper (sdfiana032): writes .heartbeat-sdfiana032" test -e "$D/.heartbeat-sdfiana032"
set_pod
expect "wrapper (sdfiana032): pod's guard refuses while it runs" \
    sh -c '! sh "$1" --check-only 2>/dev/null' _ "$GUARD"
set_ana
kill -TERM "$wpid"; finish
expect "wrapper (sdfiana032): clean exit (got $wrc)" test "$wrc" = 0
expect "wrapper (sdfiana032): released sdfiana032/<wrapper pid>" owner_is "released sdfiana032/$wpid"
expect "wrapper (sdfiana032): heartbeat removed" test ! -e "$D/.heartbeat-sdfiana032"
set_pod; guard
expect "after sdfiana032 releases, pod may start" passed

echo
echo "behaviour_test: $pass passed, $fail failed"
[ "$fail" = 0 ]
