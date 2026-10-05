#!/bin/sh
# owner-guard.sh: decide whether this side may start the River ClickHouse
# server on the shared data directory, and if so, claim it.
#
# The same script runs on both sides of the failover: in the Kubernetes pod
# (as the owner-guard init container, and again from server-wrapper.sh) and on
# the failover host under Apptainer. It must stay POSIX sh, and use only tools
# present in the pinned clickhouse/clickhouse-server image (dash, coreutils,
# wget; there is no curl).
#
# Start rules; all must hold:
#   1. owner:     the owner file says "released", or names this same side.
#                 A missing owner file means "pod".
#   2. heartbeat: the other side's heartbeat file is absent or stale.
#   3. ping:      the other side's server does not answer GET /ping
#                 (3 s timeout, no proxy). Fails closed: only a network
#                 failure counts as "not answering".
#   4. host:      if RNF_EXPECT_HOST is set, `hostname -s` equals it.
#
# Rules 1-3 and the owner write are one critical section under the claim lock,
# the directory .owner.lock (mkdir is atomic on the shared filesystem). After
# the write, the guard waits 2 s and re-reads the owner file, and requires the
# exact line it wrote.
#
# Usage:
#   owner-guard.sh               apply the rules; on success claim and exit 0,
#                                printing "owner-guard: claimed: <line>" and,
#                                if it replaced one, "owner-guard: replaced:
#                                <previous line>"
#   owner-guard.sh --check-only  apply the rules; write nothing, take no lock
#   owner-guard.sh --replace EXPECTED NEW
#                                under the claim lock, replace the owner line
#                                with NEW if it is exactly EXPECTED (EXPECTED
#                                "-" means: the file is missing). No rules.
#                                Every other writer of .owner uses this.
# On refusal: one line on stderr naming the failed rule, exit 1.
#
# Inputs (environment only):
#   RNF_SIDE               this side: "pod" or the failover host's short name
#   RNF_OTHER_SIDE         the other side
#   RNF_OTHER_PING_URL     the other side's /ping URL
#   RNF_IDENT              identity written to the owner line (default: $$)
#   RNF_EXPECT_HOST        if set, refuse unless `hostname -s` equals it
#   RNF_DATA_DIR           data directory (default /var/lib/clickhouse)
#   RNF_STALE_SECONDS      heartbeat age that counts as stale (default 120)
#
# Not handled here, deliberately: two instances of the SAME side (such as a
# force-deleted Terminating pod and its replacement) both pass rule 1. That is
# a runbook matter, as is the failover side's --force-takeover.

set -u

me="owner-guard"
lock_wait=30      # seconds to keep retrying the claim lock
lock_stale=120    # seconds after which a claim lock may be removed
verify_delay=2    # seconds between the owner write and its re-read

mode=claim
case "${1-}" in
    --check-only) mode=check ;;
    --replace)
        mode=replace
        if [ "$#" != 3 ]; then
            echo "$me: usage: $0 --replace EXPECTED NEW" >&2
            exit 2
        fi
        expected="$2"
        new_line="$3"
        ;;
    "") ;;
    *)
        echo "$me: unknown argument: $1 (accepted: --check-only, --replace)" >&2
        exit 2
        ;;
esac

side="${RNF_SIDE-}"
other="${RNF_OTHER_SIDE-}"
ping_url="${RNF_OTHER_PING_URL-}"
ident="${RNF_IDENT:-$$}"
data_dir="${RNF_DATA_DIR:-/var/lib/clickhouse}"
stale="${RNF_STALE_SECONDS:-120}"

refuse() {
    echo "$me: refusing to start ${side:-?}: $*" >&2
    exit 1
}

utc_now() {
    date -u +%Y-%m-%dT%H:%M:%SZ
}

[ -n "$side" ] || refuse "config: RNF_SIDE is not set"
[ -d "$data_dir" ] || refuse "config: data directory $data_dir does not exist"

owner_file="$data_dir/.owner"
lock_dir="$data_dir/.owner.lock"
tmp="$owner_file.tmp.$side.$$"

# The claim lock. Released on every exit path once taken.
have_lock=0
release_lock() {
    if [ "$have_lock" = 1 ]; then
        rm -rf "$lock_dir"
        have_lock=0
    fi
    rm -f "$tmp"
}
trap 'release_lock' EXIT
trap 'exit 143' TERM
trap 'exit 130' INT

take_lock() {
    deadline=$(($(date +%s) + lock_wait))
    while :; do
        if mkdir "$lock_dir" 2>/dev/null; then
            have_lock=1
            printf '%s %s %s\n' "$side" "$ident" "$(utc_now)" >"$lock_dir/holder" \
                || refuse "lock: cannot write $lock_dir/holder"
            return 0
        fi
        [ -d "$lock_dir" ] || refuse "lock: cannot create $lock_dir"
        lmtime="$(stat -c %Y "$lock_dir" 2>/dev/null)"
        if [ -n "$lmtime" ] && [ $(($(date +%s) - lmtime)) -gt "$lock_stale" ]; then
            holder="$(cat "$lock_dir/holder" 2>/dev/null)"
            echo "$me: removing a claim lock older than ${lock_stale}s (holder: ${holder:-unknown})" >&2
            # Rename first, so that of several removers only one succeeds.
            if mv "$lock_dir" "$lock_dir.stale.$side.$$" 2>/dev/null; then
                rm -rf "$lock_dir.stale.$side.$$"
            fi
            continue
        fi
        if [ "$(date +%s)" -ge "$deadline" ]; then
            holder="$(cat "$lock_dir/holder" 2>/dev/null)"
            refuse "lock: $lock_dir still held after ${lock_wait}s (holder: ${holder:-unknown})"
        fi
        sleep 1
    done
}

read_owner() {
    # Sets owner_line ("" when missing) and owner_present (0/1).
    owner_line=""
    owner_present=0
    if [ -e "$owner_file" ]; then
        owner_present=1
        if ! { IFS= read -r owner_line <"$owner_file"; } 2>/dev/null && [ -z "$owner_line" ]; then
            return 1
        fi
    fi
    return 0
}

write_owner() {
    # write_owner <line>: atomically, temp file in the same directory and
    # rename; then wait and re-read, requiring exactly that line.
    if ! printf '%s\n' "$1" >"$tmp" || ! mv -f "$tmp" "$owner_file"; then
        refuse "claim: could not write $owner_file"
    fi
    sleep "$verify_delay"
    read_owner || refuse "claim: could not re-read $owner_file"
    [ "$owner_line" = "$1" ] \
        || refuse "claim: $owner_file changed under us after the write (now: $owner_line)"
}

if [ "$mode" = replace ]; then
    take_lock
    read_owner || refuse "replace: owner file $owner_file is unreadable"
    if [ "$expected" = "-" ]; then
        [ "$owner_present" = 0 ] || refuse "replace: owner file exists ($owner_line), expected none"
    else
        [ "$owner_present" = 1 ] && [ "$owner_line" = "$expected" ] \
            || refuse "replace: owner line is '${owner_line:-(missing)}', expected '$expected'"
    fi
    write_owner "$new_line"
    echo "$me: replaced owner line with: $new_line"
    exit 0
fi

[ -n "$other" ] || refuse "config: RNF_OTHER_SIDE is not set"
[ -n "$ping_url" ] || refuse "config: RNF_OTHER_PING_URL is not set"
[ "$side" != "$other" ] || refuse "config: RNF_SIDE and RNF_OTHER_SIDE are both '$side'"
[ "$side" != "released" ] && [ "$other" != "released" ] \
    || refuse "config: 'released' is not a side"
case "$stale" in
    ''|*[!0-9]*) refuse "config: RNF_STALE_SECONDS must be a whole number, not '$stale'" ;;
esac
other_hb="$data_dir/.heartbeat-$other"

# Rule 4 first, outside the lock: it is a property of this host.
if [ -n "${RNF_EXPECT_HOST-}" ]; then
    host="$(hostname -s 2>/dev/null)"
    [ "$host" = "$RNF_EXPECT_HOST" ] \
        || refuse "rule 4 (host): this host is '$host', not the configured failover host '$RNF_EXPECT_HOST'"
fi

[ "$mode" = check ] || take_lock

# Rule 1: owner.
read_owner || refuse "rule 1 (owner): owner file $owner_file is empty or unreadable"
if [ "$owner_present" = 1 ]; then
    [ -n "$owner_line" ] || refuse "rule 1 (owner): owner file $owner_file is empty or unreadable"
    owner_state="${owner_line%% *}"
    shown="$owner_line"
else
    owner_state="pod"
    shown="(missing, which means pod)"
fi
if [ "$owner_state" != "released" ] && [ "$owner_state" != "$side" ]; then
    if [ "$owner_state" = "$other" ]; then
        refuse "rule 1 (owner): the owner file names the other side: $shown"
    fi
    refuse "rule 1 (owner): the owner file names neither this side nor released: $shown"
fi

# Rule 2: the other side's heartbeat is absent or stale. A heartbeat from the
# future (clock skew) counts as fresh.
if [ -e "$other_hb" ]; then
    mtime="$(stat -c %Y "$other_hb" 2>/dev/null)" \
        || refuse "rule 2 (heartbeat): cannot read the mtime of $other_hb"
    age=$(($(date +%s) - mtime))
    if [ "$age" -le "$stale" ]; then
        refuse "rule 2 (heartbeat): $other_hb is ${age}s old, not stale (stale means older than ${stale}s)"
    fi
fi

# Rule 3: the other side's server must not answer /ping, and this fails
# closed. Only wget's exit 4 (network failure: connection refused, timeout,
# or DNS failure) counts as "not answering"; any other status (0 answered,
# 6 auth, 8 HTTP error, 1 generic, ...) refuses. A DNS failure passes because
# rule 1, not the ping, is the fence: the ping only catches a server whose
# owner line was overwritten by hand.
# --no-proxy, and the proxy variables cleared, so no proxy can answer for it.
ping_rc=0
env -u http_proxy -u HTTP_PROXY -u https_proxy -u HTTPS_PROXY \
    -u no_proxy -u NO_PROXY \
    wget --quiet --no-proxy --tries=1 --timeout=3 --output-document=/dev/null \
    "$ping_url" >/dev/null 2>&1 || ping_rc=$?
case "$ping_rc" in
    4) ;;
    0) refuse "rule 3 (ping): the other side answers at $ping_url" ;;
    *) refuse "rule 3 (ping): $ping_url did not fail with a network error (wget status $ping_rc), so something may be answering" ;;
esac

if [ "$mode" = check ]; then
    echo "$me: $side may start (owner: $shown); --check-only, nothing written"
    exit 0
fi

# Claim. (write_owner re-reads the file, so keep what it replaced first.)
replaced_present="$owner_present"
claim="$side $ident $(utc_now)"
write_owner "$claim"
echo "$me: claimed: $claim"
if [ "$replaced_present" = 1 ]; then
    echo "$me: replaced: $shown"
fi
exit 0
