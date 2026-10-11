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
# exact line it wrote. The lock's holder file must still name this guard just
# before the write and after the re-read. A stale lock (older than 120 s) is
# removed automatically only if its holder is this same side; the other
# side's stale lock, or one with no holder, refuses (the other side may only
# be stalled, as in an NFS hang): remove it by hand once the other side is
# confirmed gone. A signal after the write puts the previous line back.
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
    if [ "$mode" = replace ]; then
        echo "$me: --replace refused: $*" >&2
    else
        echo "$me: refusing to start ${side:-?}: $*" >&2
    fi
    exit 1
}

utc_now() {
    date -u +%Y-%m-%dT%H:%M:%SZ
}

[ -n "$side" ] || refuse "config: RNF_SIDE is not set"
[ -d "$data_dir" ] || refuse "config: data directory $data_dir does not exist"

owner_file="$data_dir/.owner"
lock_dir="$data_dir/.owner.lock"
holder_file="$lock_dir/holder"
tmp="$owner_file.tmp.$side.$$"
runbook="remove .owner.lock only after confirming the other side is gone (runbook)"

# The claim lock: the directory .owner.lock, whose holder file names who
# holds it as "<side> <ident> <UTC time>". It is only ever removed by whoever
# its holder file names (or, once stale, by the same side), never blindly.
#
# On NFSv3 a retransmitted MKDIR can report EEXIST for a directory this very
# call created. That fails closed: the lock then looks held (by nobody, or by
# an unreadable holder) and the guard waits and refuses; it never proceeds
# without the lock.
# The fourth field, this process's PID, keeps two guards of one side with the
# same ident in the same second apart; readers use only the first three.
my_holder="$side $ident $(utc_now) $$"
made_lock=0       # our mkdir succeeded
acquired=0        # ... and our holder file is in place: the lock is ours
holder_is_mine() {
    _h=""
    { IFS= read -r _h <"$holder_file"; } 2>/dev/null
    [ -n "$_h" ] && [ "$_h" = "$my_holder" ]
}

# Signals: once this guard's claim is in the owner file but before it has
# exited 0, put the previous line back (under the lock it still holds), so
# that an interrupted claim leaves no trace. A claim over a missing file is
# left in place: "pod <name>" and a missing file mean the same.
claim=""
prev_line=""
on_signal() {
    if [ -n "$claim" ] && [ -n "$prev_line" ] && [ "$acquired" = 1 ] && holder_is_mine; then
        _cur=""
        { IFS= read -r _cur <"$owner_file"; } 2>/dev/null
        if [ "$_cur" = "$claim" ] \
            && printf '%s\n' "$prev_line" >"$tmp" && mv -f -T "$tmp" "$owner_file"; then
            echo "$me: interrupted after claiming; restored the owner line: $prev_line" >&2
        fi
    fi
    exit "$1"
}

release_lock() {
    # Our holder temp file first: left inside, it would keep the rmdir below
    # from removing our own empty lock, leaving a lock with no holder.
    rm -f "$tmp" "$holder_file.tmp.$side.$$"
    if [ "$acquired" = 1 ] && holder_is_mine; then
        rm -rf "$lock_dir"
    elif [ "$made_lock" = 1 ] && [ "$acquired" = 0 ] && [ ! -e "$holder_file" ]; then
        # Stopped between our mkdir and the holder rename: the directory is
        # ours. rmdir removes it only if it is still empty.
        rmdir "$lock_dir" 2>/dev/null
    fi
}
trap 'release_lock' EXIT
trap 'on_signal 143' TERM
trap 'on_signal 130' INT

take_lock() {
    deadline=$(($(date +%s) + lock_wait))
    while :; do
        if mkdir "$lock_dir" 2>/dev/null; then
            made_lock=1
            if ! printf '%s\n' "$my_holder" >"$holder_file.tmp.$side.$$" \
                || ! mv -f -T "$holder_file.tmp.$side.$$" "$holder_file"; then
                refuse "lock: cannot write $holder_file"
            fi
            acquired=1
            return 0
        fi
        if [ ! -d "$lock_dir" ]; then
            # Either it was released between our mkdir and this check (retry),
            # or we cannot create it at all.
            [ -w "$data_dir" ] || refuse "lock: cannot create $lock_dir"
            [ "$(date +%s)" -lt "$deadline" ] || refuse "lock: could not take $lock_dir within ${lock_wait}s"
            continue
        fi
        holder=""
        { IFS= read -r holder <"$holder_file"; } 2>/dev/null
        lmtime="$(stat -c %Y "$lock_dir" 2>/dev/null)"
        if [ -n "$lmtime" ] && [ $(($(date +%s) - lmtime)) -gt "$lock_stale" ]; then
            # Stale. Only this side's own stale lock may be removed
            # automatically; the other side's holder may only be stalled.
            if [ -z "$holder" ]; then
                refuse "lock: $lock_dir is older than ${lock_stale}s and has no readable holder; $runbook"
            fi
            if [ "${holder%% *}" != "$side" ]; then
                refuse "lock: $lock_dir is older than ${lock_stale}s but held by the other side ($holder); $runbook"
            fi
            echo "$me: removing this side's claim lock older than ${lock_stale}s (holder: $holder)" >&2
            # Rename to a unique name, then make sure what was renamed is the
            # lock judged stale and not a fresh one taken meanwhile.
            aside="$lock_dir.stale.$side.$$"
            if mv -T "$lock_dir" "$aside" 2>/dev/null; then
                moved=""
                { IFS= read -r moved <"$aside/holder"; } 2>/dev/null
                if [ "$moved" = "$holder" ]; then
                    rm -rf "$aside"
                elif ! mv -T "$aside" "$lock_dir" 2>/dev/null; then
                    refuse "lock: renamed a live lock ($moved) aside to $aside and could not put it back; $runbook"
                fi
            fi
            continue
        fi
        if [ "$(date +%s)" -ge "$deadline" ]; then
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
    # write_owner <line>: atomically (temp file in the same directory, then
    # rename), only while the lock is still ours; then wait, re-read, and
    # require exactly that line, and the lock still ours.
    printf '%s\n' "$1" >"$tmp" || refuse "claim: could not write $tmp"
    holder_is_mine || refuse "claim: the claim lock is no longer ours (holder: $(cat "$holder_file" 2>/dev/null)); nothing written"
    claim="$1"
    mv -f -T "$tmp" "$owner_file" || refuse "claim: could not rename $tmp to $owner_file"
    sleep "$verify_delay" &
    wait $!
    read_owner || refuse "claim: could not re-read $owner_file"
    [ "$owner_line" = "$1" ] \
        || refuse "claim: $owner_file changed under us after the write (now: $owner_line)"
    holder_is_mine || refuse "claim: the claim lock was taken over during the verify (holder: $(cat "$holder_file" 2>/dev/null))"
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
    [ "$expected" = "-" ] || prev_line="$expected"
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
[ "$owner_present" = 1 ] && prev_line="$owner_line"
line="$side $ident $(utc_now)"
write_owner "$line"
echo "$me: claimed: $line"
if [ "$replaced_present" = 1 ]; then
    echo "$me: replaced: $shown"
fi
exit 0
