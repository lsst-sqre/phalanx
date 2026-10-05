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
#                 (3 s timeout, no proxy).
#   4. host:      if RNF_EXPECT_HOST is set, `hostname -s` equals it.
#
# On success, writes "<side> <ident> <UTC time>" to the owner file atomically
# and exits 0. On refusal, prints one line naming the failed rule and exits 1.
# With --check-only, evaluates the rules and writes nothing.
#
# Inputs (environment only):
#   RNF_SIDE               this side: "pod" or the failover host's short name
#   RNF_OTHER_SIDE         the other side
#   RNF_OTHER_PING_URL     the other side's /ping URL
#   RNF_IDENT              identity written to the owner line (default: $$)
#   RNF_EXPECT_HOST        if set, refuse unless `hostname -s` equals it
#   RNF_DATA_DIR           data directory (default /var/lib/clickhouse)
#   RNF_STALE_SECONDS      heartbeat age that counts as stale (default 120)

set -u

me="owner-guard"

check_only=0
case "${1-}" in
    --check-only) check_only=1 ;;
    "") ;;
    *)
        echo "$me: unknown argument: $1 (only --check-only is accepted)" >&2
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

[ -n "$side" ] || refuse "config: RNF_SIDE is not set"
[ -n "$other" ] || refuse "config: RNF_OTHER_SIDE is not set"
[ -n "$ping_url" ] || refuse "config: RNF_OTHER_PING_URL is not set"
[ "$side" != "$other" ] || refuse "config: RNF_SIDE and RNF_OTHER_SIDE are both '$side'"
[ "$side" != "released" ] && [ "$other" != "released" ] \
    || refuse "config: 'released' is not a side"
case "$stale" in
    ''|*[!0-9]*) refuse "config: RNF_STALE_SECONDS must be a whole number, not '$stale'" ;;
esac
[ -d "$data_dir" ] || refuse "config: data directory $data_dir does not exist"

owner_file="$data_dir/.owner"
other_hb="$data_dir/.heartbeat-$other"

# Rule 4 first: it is a property of this host, independent of the shared state.
if [ -n "${RNF_EXPECT_HOST-}" ]; then
    host="$(hostname -s 2>/dev/null)"
    [ "$host" = "$RNF_EXPECT_HOST" ] \
        || refuse "rule 4 (host): this host is '$host', not the configured failover host '$RNF_EXPECT_HOST'"
fi

# Rule 1: owner.
if [ -e "$owner_file" ]; then
    owner_line=""
    if ! IFS= read -r owner_line <"$owner_file" && [ -z "$owner_line" ]; then
        refuse "rule 1 (owner): owner file $owner_file is empty or unreadable"
    fi
    # The first word is the state.
    owner_state="${owner_line%% *}"
else
    owner_line="(missing, which means pod)"
    owner_state="pod"
fi
if [ "$owner_state" != "released" ] && [ "$owner_state" != "$side" ]; then
    if [ "$owner_state" = "$other" ]; then
        refuse "rule 1 (owner): the owner file names the other side: $owner_line"
    fi
    refuse "rule 1 (owner): the owner file names neither this side nor released: $owner_line"
fi

# Rule 2: the other side's heartbeat is absent or stale.
if [ -e "$other_hb" ]; then
    mtime="$(stat -c %Y "$other_hb" 2>/dev/null)" \
        || refuse "rule 2 (heartbeat): cannot read the mtime of $other_hb"
    now="$(date +%s)"
    age=$((now - mtime))
    if [ "$age" -le "$stale" ]; then
        refuse "rule 2 (heartbeat): $other_hb is ${age}s old, not stale (stale means older than ${stale}s)"
    fi
fi

# Rule 3: the other side's server must not answer /ping. wget exits 0 on a 2xx
# answer and 8 on an HTTP error answer; both mean a server is there, so both
# refuse. Anything else (connection refused, timeout, DNS failure) passes.
# --no-proxy, and the proxy variables cleared, so no proxy can answer for it.
ping_rc=0
env -u http_proxy -u HTTP_PROXY -u https_proxy -u HTTPS_PROXY \
    -u no_proxy -u NO_PROXY \
    wget --quiet --no-proxy --tries=1 --timeout=3 --output-document=/dev/null \
    "$ping_url" >/dev/null 2>&1 || ping_rc=$?
case "$ping_rc" in
    0) refuse "rule 3 (ping): the other side answers at $ping_url" ;;
    8) refuse "rule 3 (ping): a server answers (with an HTTP error) at $ping_url" ;;
esac

if [ "$check_only" = 1 ]; then
    echo "$me: $side may start (owner: $owner_line); --check-only, nothing written"
    exit 0
fi

# Claim: write the owner line atomically (temp file in the same directory, then
# rename).
tmp="$owner_file.tmp.$$"
if ! printf '%s %s %s\n' "$side" "$ident" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >"$tmp" \
    || ! mv -f "$tmp" "$owner_file"; then
    rm -f "$tmp"
    refuse "claim: could not write $owner_file"
fi
echo "$me: $side claimed $data_dir as $side $ident"
exit 0
