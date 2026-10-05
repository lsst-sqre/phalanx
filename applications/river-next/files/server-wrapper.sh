#!/bin/sh
# server-wrapper.sh: run the River ClickHouse server under the failover
# ownership protocol.
#
# The same script runs on both sides of the failover: as the ClickHouse
# container's command in the Kubernetes pod, and as the Apptainer instance's
# process on the failover host. It must stay POSIX sh, and use only tools
# present in the pinned clickhouse/clickhouse-server image.
#
#   1. Run owner-guard.sh (next to this script), which applies the start rules
#      and writes the owner line "<side> <ident>". Exit with its status if it
#      refuses, without starting the server.
#   2. Start clickhouse-server --config-file=/etc/clickhouse-server/config.xml
#      (plus any arguments given to this script) as a child process, and a
#      heartbeat loop beside it that touches .heartbeat-<side> every
#      RNF_HEARTBEAT_SECONDS for as long as the server is alive.
#   3. Forward SIGTERM and SIGINT to the server, and wait for it to exit.
#   4. On exit 0, write "released <side>/<ident>"; on any other exit, leave the
#      owner line alone so this side may restart. Remove the heartbeat either
#      way.
#   5. Exit with the server's exit status.
#
# What the image's /entrypoint.sh does that matters for a non-root user with
# existing data, users fully defined in users.d (CLICKHOUSE_SKIP_USER_SETUP=1),
# and no initdb scripts, is reproduced here: CLICKHOUSE_WATCHDOG_ENABLE
# defaults to 0, the working directory is the data directory, and the server is
# started with the same --config-file. Its `clickhouse su <uid>:<gid>` is a
# no-op for a non-root user, and the directories it pre-creates are all
# created by the server itself.
#
# Inputs (environment only): RNF_SIDE, RNF_OTHER_SIDE, RNF_OTHER_PING_URL,
# RNF_IDENT (default: this script's PID), RNF_EXPECT_HOST, RNF_DATA_DIR
# (default /var/lib/clickhouse), RNF_HEARTBEAT_SECONDS (default 30) and
# RNF_STALE_SECONDS (default 120). See owner-guard.sh.

set -u

me="server-wrapper"

side="${RNF_SIDE-}"
data_dir="${RNF_DATA_DIR:-/var/lib/clickhouse}"
heartbeat="${RNF_HEARTBEAT_SECONDS:-30}"
ident="${RNF_IDENT:-$$}"

case "$heartbeat" in
    ''|*[!0-9]*|0)
        echo "$me: RNF_HEARTBEAT_SECONDS must be a positive whole number, not '$heartbeat'" >&2
        exit 1
        ;;
esac

here="$(dirname "$0")"

# 1. Start rules and the owner line. The guard reads the same environment; the
# identity is fixed here so that the owner line and the released line agree.
RNF_IDENT="$ident" sh "$here/owner-guard.sh" || exit $?

owner_file="$data_dir/.owner"
hb_file="$data_dir/.heartbeat-$side"

write_atomic() {
    # write_atomic <file> <content>: temp file in the same directory, then
    # rename.
    _tmp="$1.tmp.$$"
    if printf '%s\n' "$2" >"$_tmp" && mv -f "$_tmp" "$1"; then
        return 0
    fi
    rm -f "$_tmp"
    return 1
}

utc_now() {
    date -u +%Y-%m-%dT%H:%M:%SZ
}

# As the image's entrypoint does: no watchdog process between us and the
# server, and the data directory as the working directory.
: "${CLICKHOUSE_WATCHDOG_ENABLE:=0}"
export CLICKHOUSE_WATCHDOG_ENABLE
cd "$data_dir" || { echo "$me: cannot cd to $data_dir" >&2; exit 1; }

# Install the traps before the server starts, so that a signal arriving during
# startup is not lost: it is recorded and forwarded once the server exists.
server_pid=""
pending=""
got_signal=0
forward() {
    got_signal=1
    if [ -n "$server_pid" ]; then
        echo "$me: received SIG$1, forwarding it to clickhouse-server (pid $server_pid)" >&2
        kill -s "$1" "$server_pid" 2>/dev/null
    else
        pending="$1"
    fi
}
trap 'forward TERM' TERM
trap 'forward INT' INT

# 2. The server, then the heartbeat loop. A background command in a
# non-interactive shell starts with SIGINT ignored; clickhouse-server installs
# its own handlers for SIGINT and SIGTERM, so forwarding still works.
clickhouse-server --config-file=/etc/clickhouse-server/config.xml "$@" &
server_pid=$!
echo "$me: $side started clickhouse-server (pid $server_pid) as $side $ident" >&2
if [ -n "$pending" ]; then
    forward "$pending"
fi

(
    # Traps are reset in this subshell. It is stopped with SIGTERM by the
    # wrapper when the server exits, and stops by itself if the server
    # disappears while the wrapper is gone.
    while kill -0 "$server_pid" 2>/dev/null; do
        write_atomic "$hb_file" "$(utc_now)" \
            || echo "$me: could not write heartbeat $hb_file" >&2
        sleep "$heartbeat"
    done
) &
hb_pid=$!

# 3. Wait for the server. A trapped signal interrupts `wait` (status > 128);
# the trap forwards it, and we wait again until the server itself exits.
rc=0
last=0
while :; do
    got_signal=0
    wait "$server_pid"
    rc=$?
    if [ "$got_signal" = 0 ]; then
        break
    fi
    # 127: the shell already collected the server's status in the wait that
    # the signal interrupted; keep that one.
    if [ "$rc" = 127 ] && ! kill -0 "$server_pid" 2>/dev/null; then
        rc=$last
        break
    fi
    last=$rc
done

# The heartbeat stops with the server.
kill -s TERM "$hb_pid" 2>/dev/null
wait "$hb_pid" 2>/dev/null
rm -f "$hb_file" "$hb_file.tmp.$$"

# 4. Release on a clean exit only.
if [ "$rc" = 0 ]; then
    if write_atomic "$owner_file" "released $side/$ident $(utc_now)"; then
        echo "$me: clickhouse-server exited cleanly; wrote released $side/$ident" >&2
    else
        echo "$me: clickhouse-server exited cleanly, but writing $owner_file failed" >&2
    fi
else
    echo "$me: clickhouse-server exited with status $rc; owner line left as $side $ident" >&2
fi

# 5.
exit "$rc"
