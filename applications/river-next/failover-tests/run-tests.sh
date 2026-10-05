#!/bin/bash
# Tests for river-next's ClickHouse failover support. One command:
#
#     applications/river-next/failover-tests/run-tests.sh
#
# These run by hand, not in CI: they need Apptainer and the pinned image, and
# they are not helm-unittest suites (this directory is deliberately not named
# tests/, and .helmignore keeps it out of the chart package).
#
# 1. sh -n (and ShellCheck, if installed) on the two failover scripts.
# 2. render_test.py: both clickhouse.backend renders. Needs helm, and a Python
#    with phalanx and PyYAML (the workspace venv); set RIVER_TEST_PYTHON to
#    pick it, otherwise `python3` on PATH is used.
# 3. behaviour_test.sh: every guard rule and the wrapper's exit paths, with a
#    stub server. Runs inside the pinned ClickHouse image under Apptainer, so
#    it meets the image's dash and wget; without Apptainer it falls back to
#    the host's sh, and says so.
# 4. real_server_test.sh: the wrapper around the image's real
#    clickhouse-server, on non-default ports and a throwaway directory.
#    Needs Apptainer; skipped (and said so) without it.
#
# The image is the chart's pinned clickhouse.image, pulled with Apptainer's
# docker:// transport; set RIVER_TEST_SIF to a local SIF of it to skip the
# pull. RIVER_TEST_SKIP may list any of: render behaviour real.
#
# Scratch goes under RIVER_TEST_TMP (default: a new directory under TMPDIR).

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
CHART="$(dirname "$HERE")"
SCRIPTS="$CHART/files"
SKIP=" ${RIVER_TEST_SKIP:-} "
PY="${RIVER_TEST_PYTHON:-python3}"
results=()
status=0

record() {
    # record <name> <status>
    if [ "$2" = 0 ]; then
        results+=("PASS  $1")
    elif [ "$2" = skip ]; then
        results+=("SKIP  $1")
    else
        results+=("FAIL  $1")
        status=1
    fi
}

TMP="${RIVER_TEST_TMP:-$(mktemp -d "${TMPDIR:-/tmp}/river-failover-test.XXXXXX")}"
mkdir -p "$TMP"
TMP="$(cd "$TMP" && pwd)"
cleanup() {
    [ -n "${http_pid:-}" ] && kill "$http_pid" 2>/dev/null
    rm -rf "$TMP"
}
trap cleanup EXIT

# The pinned image.
if [ -n "${RIVER_TEST_SIF:-}" ]; then
    IMAGE="$RIVER_TEST_SIF"
else
    repo=$(awk '/^clickhouse:/{c=1} c&&/^    repository:/{print $2; exit}' "$CHART/values.yaml" | tr -d '"')
    tag=$(awk '/^clickhouse:/{c=1} c&&/^    tag:/{print $2; exit}' "$CHART/values.yaml" | tr -d '"')
    digest=$(awk '/^clickhouse:/{c=1} c&&/^    digest:/{print $2; exit}' "$CHART/values.yaml" | tr -d '"')
    # Apptainer refuses a reference with both a tag and a digest; the digest
    # is what pins it.
    IMAGE="docker://$repo@$digest"
    echo "image: $IMAGE (tag $tag)"
fi
have_apptainer=0
if command -v apptainer >/dev/null 2>&1; then
    echo "=== 0. image"
    if timeout 1800 apptainer exec "$IMAGE" true 2> >(grep -v '^INFO:' >&2); then
        have_apptainer=1
        record "pinned image runs under Apptainer" 0
    else
        record "pinned image runs under Apptainer ($IMAGE)" 1
    fi
fi

echo "=== 1. syntax"
rc=0
for f in "$SCRIPTS/owner-guard.sh" "$SCRIPTS/server-wrapper.sh"; do
    sh -n "$f" || rc=1
done
record "sh -n (host sh)" "$rc"
if [ "$have_apptainer" = 1 ]; then
    timeout 900 apptainer exec --bind "$CHART" "$IMAGE" sh -c 'sh -n "$1" && sh -n "$2"' _ \
        "$SCRIPTS/owner-guard.sh" "$SCRIPTS/server-wrapper.sh" 2> >(grep -v '^INFO:' >&2)
    record "sh -n (the image's dash)" $?
fi
if command -v shellcheck >/dev/null 2>&1; then
    shellcheck -s sh "$SCRIPTS/owner-guard.sh" "$SCRIPTS/server-wrapper.sh" "$HERE/behaviour_test.sh"
    record "shellcheck" $?
else
    echo "shellcheck not installed; skipped"
    record "shellcheck (not installed)" skip
fi

echo "=== 2. render"
if [[ "$SKIP" == *" render "* ]]; then
    record "render_test.py" skip
else
    timeout 900 "$PY" "$HERE/render_test.py"
    record "render_test.py" $?
fi

# Fake /ping endpoints: a local HTTP server whose /ping answers "Ok.", any
# other path 404, and a port with nothing listening.
free_port() {
    python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])'
}
mkdir -p "$TMP/www"
printf 'Ok.\n' >"$TMP/www/ping"
http_port=$(free_port)
(cd "$TMP/www" && exec timeout 3600 python3 -m http.server --bind 127.0.0.1 "$http_port" >/dev/null 2>&1) &
http_pid=$!
closed_port=$(free_port)
for _ in $(seq 50); do
    curl --noproxy '*' -s -o /dev/null "http://127.0.0.1:$http_port/ping" && break
    sleep 0.1
done
export PING_OK_URL="http://127.0.0.1:$http_port/ping"
export PING_ERR_URL="http://127.0.0.1:$http_port/no-such-path"
export PING_CLOSED_URL="http://127.0.0.1:$closed_port/ping"
export PROXY_URL="http://127.0.0.1:$http_port/"

echo "=== 3. behaviour"
if [[ "$SKIP" == *" behaviour "* ]]; then
    record "behaviour_test.sh" skip
else
    mkdir -p "$TMP/behaviour"
    export SCRIPTS STUB_DIR="$HERE/stub" WORK="$TMP/behaviour"
    if [ "$have_apptainer" = 1 ]; then
        timeout 900 apptainer exec --bind "$CHART" --bind "$TMP" "$IMAGE" \
            sh "$HERE/behaviour_test.sh" 2> >(grep -v '^INFO:' >&2)
        record "behaviour_test.sh (in the ClickHouse image)" $?
    else
        echo "apptainer not available: running with the host's sh instead"
        timeout 900 sh "$HERE/behaviour_test.sh"
        record "behaviour_test.sh (host sh, NOT the image)" $?
    fi
fi

echo "=== 4. real clickhouse-server"
if [[ "$SKIP" == *" real "* ]]; then
    record "real_server_test.sh" skip
elif [ "$have_apptainer" = 0 ]; then
    echo "apptainer not available; skipped"
    record "real_server_test.sh (no apptainer)" skip
else
    mkdir -p "$TMP/real"
    timeout 1200 env IMAGE="$IMAGE" WORK="$TMP/real" SCRIPTS="$SCRIPTS" PY="$PY" \
        bash "$HERE/real_server_test.sh"
    record "real_server_test.sh" $?
fi

echo
echo "=== summary"
printf '%s\n' "${results[@]}"
exit "$status"
