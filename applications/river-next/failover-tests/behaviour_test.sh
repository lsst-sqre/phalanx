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
#   PING_AUTH_URL    answers 401
#   PING_CLOSED_URL  nothing listening
#   PROXY_URL        an HTTP server that would answer any proxied request

set -u

: "${SCRIPTS:?}" "${STUB_DIR:?}" "${WORK:?}"
: "${PING_OK_URL:?}" "${PING_ERR_URL:?}" "${PING_AUTH_URL:?}" "${PING_CLOSED_URL:?}" "${PROXY_URL:?}"

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
no_lock() { [ ! -e "$D/.owner.lock" ]; }
fresh_hb() { date -u +%Y-%m-%dT%H:%M:%SZ >"$D/.heartbeat-$1"; }
stale_hb() { fresh_hb "$1"; touch -d '-10 seconds' "$D/.heartbeat-$1"; }

echo "== owner-guard.sh ($(readlink -f /bin/sh))"

# Rule 1: owner.
set_pod; reset; guard
expect "rule 1: missing owner file means pod; pod may start" passed
expect "claim: owner line is 'pod <ident> <time>'" owner_is "pod river-next-clickhouse-0"
expect "claim: no temp file left behind" no_tmp
expect "claim: reports the line it wrote" grep -q "^owner-guard: claimed: pod river-next-clickhouse-0 " "$WORK/out"
expect "claim: reports no replaced line when there was no file" sh -c '! grep -q replaced: "$1"' _ "$WORK/out"

set_pod; reset; echo "released sdfiana032/1234 2026-10-05T00:00:00Z" >"$D/.owner"; guard
expect "rule 1: released (by the other side) lets pod start" passed
expect "rule 1: ... and pod claims it" owner_is "pod river-next-clickhouse-0"
expect "claim: reports the released line it replaced" grep -qx "owner-guard: replaced: released sdfiana032/1234 2026-10-05T00:00:00Z" "$WORK/out"

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

set_pod; reset; RNF_OTHER_PING_URL="$PING_AUTH_URL"; guard
expect "rule 3: fails closed: a 401 (wget status 6) refuses" refused "wget status 6"

set_pod; reset; RNF_OTHER_PING_URL="http://"; guard
expect "rule 3: fails closed: a generic wget error (status 1) refuses" refused "wget status 1"
expect "lock: released after a refusal inside the lock" no_lock

set_pod; reset; RNF_OTHER_PING_URL="$PING_CLOSED_URL"; guard
expect "rule 3: nothing listening (wget status 4) passes" passed
expect "lock: released after a successful claim" no_lock

set_pod; reset; RNF_OTHER_PING_URL="http://no-such-host.invalid:8123/ping"; guard
expect "rule 3: a DNS failure (wget status 4) passes; rule 1 is the fence" passed

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

# The claim lock.
set_pod; reset; echo "pod x 2026-10-05T00:00:00Z" >"$D/.owner"; chmod 000 "$D/.owner"; guard
chmod 600 "$D/.owner"
expect "lock: an unreadable owner file refuses (rule 1)" refused "rule 1 (owner)"
expect "lock: released after an error inside the lock" no_lock

set_pod; reset; mkdir "$D/.owner.lock"; echo "sdfiana032 99 2026-10-05T00:00:00Z" >"$D/.owner.lock/holder"
touch -d '-200 seconds' "$D/.owner.lock"; guard
expect "lock: a lock older than 120 s is removed and the claim proceeds" passed
expect "lock: ... with a message naming the old holder" grep -q "removing a claim lock older than 120s (holder: sdfiana032 99" "$WORK/err"
expect "lock: ... and the stale lock is gone afterwards" no_lock

set_pod; reset; mkdir "$D/.owner.lock"; echo "sdfiana032 99 2026-10-05T00:00:00Z" >"$D/.owner.lock/holder"
t0=$(date +%s); guard; t1=$(date +%s)
expect "lock: a live lock refuses after the bounded wait" refused "lock: .* still held after 30s (holder: sdfiana032 99"
expect "lock: ... which is about 30 s (took $((t1 - t0)) s)" test $((t1 - t0)) -ge 29 -a $((t1 - t0)) -le 35
expect "lock: a lock not ours is left alone" test -d "$D/.owner.lock"
expect "lock: nothing written while it was held" test ! -e "$D/.owner"

set_pod; reset; echo "released sdfiana032/1 2026-10-05T00:00:00Z" >"$D/.owner"
guard --replace "released sdfiana032/1 2026-10-05T00:00:00Z" "pod new 2026-10-05T00:00:01Z"
expect "--replace: swaps an exactly matching line" sh -c '[ "$(cat "$1")" = "pod new 2026-10-05T00:00:01Z" ]' _ "$D/.owner"
expect "--replace: releases the lock" no_lock
guard --replace "released sdfiana032/1 2026-10-05T00:00:00Z" "pod other 2026-10-05T00:00:02Z"
expect "--replace: refuses when the line differs" refused "replace: owner line is"
expect "--replace: ... and leaves it" sh -c '[ "$(cat "$1")" = "pod new 2026-10-05T00:00:01Z" ]' _ "$D/.owner"
expect "--replace: releases the lock after refusing" no_lock
reset; guard --replace - "pod first 2026-10-05T00:00:00Z"
expect "--replace -: writes when the file is missing" owner_is "pod first"
expect "claim: side-qualified temp names leave nothing behind" no_tmp

# Concurrent claims: both sides at once on a released directory; exactly one
# may win, every time.
iters=12
wins_ok=0
i=0
while [ "$i" -lt "$iters" ]; do
    reset; echo "released pod/old 2026-10-05T00:00:00Z" >"$D/.owner"
    (set_pod; sh "$GUARD" >"$WORK/c-pod.out" 2>"$WORK/c-pod.err"; echo $? >"$WORK/c-pod.rc") &
    a=$!
    (set_ana; sh "$GUARD" >"$WORK/c-ana.out" 2>"$WORK/c-ana.err"; echo $? >"$WORK/c-ana.rc") &
    b=$!
    wait "$a"; wait "$b"
    ra=$(cat "$WORK/c-pod.rc"); rb=$(cat "$WORK/c-ana.rc")
    line=$(owner)
    if [ "$ra" = 0 ] && [ "$rb" = 1 ] && [ "${line%% *}" = pod ] \
        && grep -q "rule 1 (owner)" "$WORK/c-ana.err"; then
        wins_ok=$((wins_ok + 1))
    elif [ "$ra" = 1 ] && [ "$rb" = 0 ] && [ "${line%% *}" = sdfiana032 ] \
        && grep -q "rule 1 (owner)" "$WORK/c-pod.err"; then
        wins_ok=$((wins_ok + 1))
    else
        echo "     iteration $i: pod rc=$ra ana rc=$rb owner='$line'" >&2
        cat "$WORK/c-pod.err" "$WORK/c-ana.err" >&2
    fi
    no_lock || echo "     iteration $i: lock left behind" >&2
    i=$((i + 1))
done
expect "concurrent claims: exactly one side wins, the other refuses on rule 1 ($wins_ok/$iters)" test "$wins_ok" = "$iters"
expect "concurrent claims: no lock left behind" no_lock

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
expect "wrapper: server started" wait_for 100 started
expect "wrapper: heartbeat written while the server runs" wait_for 30 test -e "$D/.heartbeat-pod"
m1=$(hb_mtime pod); sleep 2.2; m2=$(hb_mtime pod)
expect "wrapper: heartbeat refreshed every RNF_HEARTBEAT_SECONDS ($m1 -> $m2)" test "${m2:-0}" -gt "${m1:-0}"
expect "wrapper: owner line is pod <ident> while running" owner_is "pod river-next-clickhouse-0"
(RNF_SIDE=sdfiana032 RNF_OTHER_SIDE=pod; export RNF_SIDE RNF_OTHER_SIDE
    sh "$GUARD" --check-only >"$WORK/out" 2>"$WORK/err"); rc=$?
expect "wrapper: the other side's guard refuses while it runs (rule 1)" refused "rule 1 (owner)"
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
wait_for 100 started
kill -INT "$wpid"; finish
expect "wrapper: SIGINT forwarded to the server" grep -q '^signal INT' "$LOG"
expect "wrapper: exit 0 after SIGINT (got $wrc)" test "$wrc" = 0
expect "wrapper: released after SIGINT" owner_is "released pod/river-next-clickhouse-0"

# Non-zero exit after a signal: owner line kept, heartbeat gone, status passed on.
set_pod; reset
start_wrapper term3
wait_for 100 started
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
wait_for 100 started
wait_for 30 test -e "$D/.heartbeat-sdfiana032"
expect "wrapper (sdfiana032): owner line is sdfiana032 <wrapper pid>" owner_is "sdfiana032 $wpid"
expect "wrapper (sdfiana032): writes .heartbeat-sdfiana032" test -e "$D/.heartbeat-sdfiana032"
set_pod; guard --check-only
expect "wrapper (sdfiana032): pod's guard refuses while it runs (rule 1)" refused "rule 1 (owner)"
set_ana
kill -TERM "$wpid"; finish
expect "wrapper (sdfiana032): clean exit (got $wrc)" test "$wrc" = 0
expect "wrapper (sdfiana032): released sdfiana032/<wrapper pid>" owner_is "released sdfiana032/$wpid"
expect "wrapper (sdfiana032): heartbeat removed" test ! -e "$D/.heartbeat-sdfiana032"
set_pod; guard
expect "after sdfiana032 releases, pod may start" passed

# A signal while the guard runs (the hung ping holds it for 3 s): the server
# is never started, the wrapper exits 143, and a released line the claim
# replaced is put back.
set_pod; reset; echo "released sdfiana032/7 2026-10-05T00:00:00Z" >"$D/.owner"
RNF_OTHER_PING_URL="http://192.0.2.1:8123/ping"
start_wrapper term0
sleep 1; kill -TERM "$wpid"; finish
expect "signal during guard: exit 143 (got $wrc)" test "$wrc" = 143
expect "signal during guard: server never started" test ! -s "$LOG"
expect "signal during guard: the released line is restored" owner_is "released sdfiana032/7"
expect "signal during guard: no heartbeat, no lock" sh -c '[ ! -e "$1/.heartbeat-pod" ] && [ ! -e "$1/.owner.lock" ]' _ "$D"

set_pod; reset; echo "pod river-next-clickhouse-0 2026-10-05T00:00:00Z" >"$D/.owner"
RNF_OTHER_PING_URL="http://192.0.2.1:8123/ping"
start_wrapper term0
sleep 1; kill -INT "$wpid"; finish
expect "signal during guard (SIGINT): exit 143 (got $wrc)" test "$wrc" = 143
expect "signal during guard: a non-released line is left as claimed" owner_is "pod river-next-clickhouse-0"
expect "signal during guard (SIGINT): server never started" test ! -s "$LOG"

# The same as PID 1 in a PID namespace, as in the pod, where a signal with no
# handler would be dropped. unshare -f forks the wrapper as PID 1; signals
# are sent from outside to its outer PID.
if unshare -U -r -p -f --mount-proc true 2>/dev/null; then
    # start_pid1 <mode>: sets upid (unshare) and wpid (the wrapper, PID 1).
    start_pid1() {
        : >"$LOG"
        # unshare passes SIGINT and SIGTERM on ignored, and a shell cannot
        # trap a signal ignored at entry, so reset them (perl, then exec) as
        # the container runtime does for a pod's PID 1.
        STUB_MODE="$1" unshare -U -r -p -f --mount-proc \
            perl -e '$SIG{INT} = $SIG{TERM} = "DEFAULT"; exec @ARGV or die' \
            sh "$WRAPPER" >"$WORK/wout" 2>"$WORK/werr" &
        upid=$!
        wpid=""
        _n=50
        while [ -z "$wpid" ] && [ "$_n" -gt 0 ]; do
            wpid=$(ps -o pid= --ppid "$upid" 2>/dev/null | tr -d ' ')
            [ -n "$wpid" ] || sleep 0.1
            _n=$((_n - 1))
        done
    }
    finish_pid1() {
        _n=150
        while kill -0 "$upid" 2>/dev/null && [ "$_n" -gt 0 ]; do sleep 0.1; _n=$((_n - 1)); done
        if kill -0 "$upid" 2>/dev/null; then
            kill -9 "$wpid" "$upid" 2>/dev/null; wrc=timeout
        else
            wait "$upid"; wrc=$?
        fi
    }
    set_pod; reset; echo "released sdfiana032/8 2026-10-05T00:00:00Z" >"$D/.owner"
    RNF_OTHER_PING_URL="http://192.0.2.1:8123/ping"
    start_pid1 term0
    expect "PID 1: wrapper found (outer pid $wpid)" test -n "$wpid"
    sleep 1; kill -TERM "$wpid"; finish_pid1
    expect "PID 1: SIGTERM during the guard is not dropped: exit 143 (got $wrc)" test "$wrc" = 143
    expect "PID 1: server never started" test ! -s "$LOG"
    expect "PID 1: the released line is restored" owner_is "released sdfiana032/8"

    set_pod; reset
    start_pid1 term0
    wait_for 100 started
    kill -TERM "$wpid"; finish_pid1
    expect "PID 1: SIGTERM after start is forwarded; clean exit (got $wrc)" test "$wrc" = 0
    expect "PID 1: released" owner_is "released pod/river-next-clickhouse-0"
else
    bad "PID 1 tests: unshare -U -r -p -f is not available here"
fi

echo
echo "behaviour_test: $pass passed, $fail failed"
[ "$fail" = 0 ]
