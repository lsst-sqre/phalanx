"""Render assertions for river-next's clickhouse.backend switch.

Run with the Python environment that holds the phalanx CLI (it imports
phalanx to get the values Argo CD injects), from anywhere in the repository:

    python applications/river-next/failover-tests/render_test.py

The default render comes from ``phalanx application template river-next
usdfdev``. The CLI takes no extra values, so renders with overrides run
``helm template`` exactly as phalanx does (same values files, same injected
``--set``), plus one more values file; the two are first checked to agree.
"""

# A standalone test script run by hand (not a package, and outside the tests/
# trees that the shared Ruff configuration relaxes these rules for).
# ruff: noqa: INP001, D103, SLF001

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

from phalanx.factory import Factory

APP = "river-next"
ENV = "usdfdev"
HERE = Path(__file__).resolve().parent
CHART = HERE.parent
ROOT = CHART.parent.parent
FAILOVER_HOST = "sdfiana032.sdf.slac.stanford.edu"
SERVICE_HOST = "river-next-clickhouse.river-next.svc.cluster.local"
WRAPPER = ["/bin/sh", "/opt/river-failover/server-wrapper.sh"]
GUARD = ["/bin/sh", "/opt/river-failover/owner-guard.sh"]
CH_ENV = ("MPPDB_CLICKHOUSE_HOST", "MPPDB_CLICKHOUSE_PORT")

type Docs = dict[tuple[str, str], dict[str, Any]]

failures: list[str] = []


def out(line: str) -> None:
    sys.stdout.write(line + "\n")


def check(cond: object, what: str) -> None:
    out(("ok   " if cond else "FAIL ") + what)
    if not cond:
        failures.append(what)


def render_phalanx() -> str:
    exe = shutil.which("phalanx") or str(
        Path(sys.executable).parent / "phalanx"
    )
    return subprocess.run(
        [exe, "application", "template", APP, ENV],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    ).stdout


def injected_values() -> dict[str, str]:
    factory = Factory(ROOT)
    service = factory.create_application_service()
    env = factory.create_config_storage().load_environment(ENV)
    return service._build_injected_values(APP, env)


def render_helm(
    overrides: dict[str, Any] | None,
) -> subprocess.CompletedProcess[str]:
    """Run helm template as phalanx does, plus an optional override file."""
    set_arg = ",".join(f"{k}={v}" for k, v in injected_values().items())
    args = [
        "helm",
        "template",
        APP,
        str(CHART),
        "--include-crds",
        "--values",
        f"{APP}/values.yaml",
        "--values",
        f"{APP}/values-{ENV}.yaml",
        "--set",
        set_arg,
    ]
    with tempfile.TemporaryDirectory() as tmp:
        override_file = Path(tmp) / "override.yaml"
        override_file.write_text(yaml.safe_dump(overrides or {}))
        if overrides is not None:
            args += ["--values", str(override_file)]
        return subprocess.run(
            args,
            cwd=CHART.parent,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )


def docs(text: str) -> Docs:
    return {
        (d["kind"], d["metadata"]["name"]): d
        for d in yaml.safe_load_all(text)
        if d
    }


def sts(d: Docs) -> dict[str, Any]:
    return d[("StatefulSet", "river-next-clickhouse")]


def ch_container(d: Docs) -> dict[str, Any]:
    return next(
        c
        for c in sts(d)["spec"]["template"]["spec"]["containers"]
        if c["name"] == "clickhouse"
    )


def frontend(d: Docs) -> dict[str, Any]:
    spec = d[("Deployment", "river-next")]["spec"]["template"]["spec"]
    return spec["containers"][0]


def frontend_env(d: Docs) -> dict[str, Any]:
    return {e["name"]: e.get("value") for e in frontend(d)["env"]}


def rnf_env(container: dict[str, Any]) -> dict[str, Any]:
    return {
        e["name"]: e.get("value", e.get("valueFrom"))
        for e in container.get("env", [])
        if e["name"].startswith("RNF_")
    }


def strip_failover(d: Docs) -> Docs:
    """Reset the only backend-dependent fields (contract 13.10).

    These are the StatefulSet's replicas and the front end's ClickHouse host
    and port. What remains of the render must be identical across backends.
    """
    d = copy.deepcopy(d)
    sts(d)["spec"].pop("replicas")
    fc = frontend(d)
    fc["env"] = [e for e in fc["env"] if e["name"] not in CH_ENV]
    return d


def check_both(name: str, d: Docs) -> None:
    golden_file = HERE / "golden" / "clickhouse-configmap-data.json"
    golden = json.loads(golden_file.read_text())
    scripts = {
        k: (CHART / "files" / k).read_text()
        for k in ("owner-guard.sh", "server-wrapper.sh")
    }
    cm = d[("ConfigMap", "river-next-clickhouse")]
    check(
        cm["data"] == golden,
        f"{name}: river-next-clickhouse config.d/users.d data"
        " byte-identical to the pre-failover render",
    )
    fcm = d.get(("ConfigMap", "river-next-clickhouse-failover"))
    check(
        fcm is not None and fcm["data"] == scripts,
        f"{name}: river-next-clickhouse-failover holds owner-guard.sh"
        " and server-wrapper.sh verbatim",
    )
    grace = sts(d)["spec"]["template"]["spec"]["terminationGracePeriodSeconds"]
    check(grace == 300, f"{name}: terminationGracePeriodSeconds is 300")


def check_guard(name: str, pod: Docs) -> None:
    """Check the guard, which renders in both backends (contract 13.10)."""
    s = sts(pod)
    spec = s["spec"]["template"]["spec"]
    c = ch_container(pod)
    inits = spec.get("initContainers", [])
    check(
        [i["name"] for i in inits] == ["owner-guard"],
        f"{name}: one init container, owner-guard",
    )
    g = inits[0] if inits else {}
    check(
        g.get("command") == GUARD, f"{name}: owner-guard runs owner-guard.sh"
    )
    check(
        g.get("image") == c["image"],
        f"{name}: owner-guard uses the ClickHouse image",
    )
    check(
        g.get("securityContext") == c["securityContext"],
        f"{name}: owner-guard has the ClickHouse container's securityContext",
    )
    check(
        g.get("resources") == c["resources"],
        f"{name}: owner-guard has the ClickHouse container's resources"
        " (QoS unchanged)",
    )
    data_mount = next(
        m for m in c["volumeMounts"] if m["mountPath"] == "/var/lib/clickhouse"
    )
    check(
        data_mount in g.get("volumeMounts", []),
        f"{name}: owner-guard mounts the data volume at /var/lib/clickhouse",
    )
    check(
        c.get("command") == WRAPPER,
        f"{name}: ClickHouse container runs server-wrapper.sh",
    )
    want_env = {
        "RNF_SIDE": "pod",
        "RNF_IDENT": {"fieldRef": {"fieldPath": "metadata.name"}},
        "RNF_OTHER_SIDE": "sdfiana032",
        "RNF_OTHER_PING_URL": f"http://{FAILOVER_HOST}:8123/ping",
        "RNF_DATA_DIR": "/var/lib/clickhouse",
    }
    check(rnf_env(c) == want_env, f"{name}: wrapper environment per 13.8")
    check(rnf_env(g) == want_env, f"{name}: guard environment per 13.8")
    check(
        any(
            v["name"] == "failover"
            and v["configMap"]["name"] == "river-next-clickhouse-failover"
            for v in spec["volumes"]
        ),
        f"{name}: scripts volume from the failover ConfigMap",
    )


def check_external(pod: Docs, ext: Docs) -> None:
    s = sts(ext)
    spec = s["spec"]["template"]["spec"]
    c = ch_container(ext)
    check(s["spec"]["replicas"] == 0, "external: StatefulSet kept, replicas 0")
    check(
        [i["name"] for i in spec.get("initContainers", [])] == ["owner-guard"]
        and c.get("command") == WRAPPER,
        "external: guard and wrapper still in the pod template",
    )
    check(sts(pod)["spec"]["replicas"] == 1, "pod: StatefulSet replicas 1")
    fe = frontend_env(pod)
    check(
        fe["MPPDB_CLICKHOUSE_HOST"] == SERVICE_HOST
        and fe["MPPDB_CLICKHOUSE_PORT"] == "8123",
        "pod: front end uses the in-cluster Service",
    )
    fe = frontend_env(ext)
    check(
        fe["MPPDB_CLICKHOUSE_HOST"] == FAILOVER_HOST
        and fe["MPPDB_CLICKHOUSE_PORT"] == "8123",
        "external: front end points at the failover host on 8123",
    )
    check(
        strip_failover(pod) == strip_failover(ext),
        "pod vs external: only replicas and the front-end host/port differ"
        " (guard, Services, LoadBalancer, NetworkPolicy, claims, ...)",
    )
    check(set(pod) == set(ext), "pod vs external: same set of objects")


def check_overrides() -> None:
    alt_host = "failover.example.org"
    alt = render_helm(
        {"clickhouse": {"backend": "external", "external": {"host": alt_host}}}
    )
    check(
        alt.returncode == 0
        and frontend_env(docs(alt.stdout))["MPPDB_CLICKHOUSE_HOST"]
        == alt_host,
        "external: front end follows clickhouse.external.host",
    )
    alt = render_helm({"clickhouse": {"external": {"host": alt_host}}})
    env = (
        rnf_env(ch_container(docs(alt.stdout))) if alt.returncode == 0 else {}
    )
    check(
        env.get("RNF_OTHER_SIDE") == "failover"
        and env.get("RNF_OTHER_PING_URL") == f"http://{alt_host}:8123/ping",
        "pod: guard follows clickhouse.external.host",
    )

    # Invalid settings fail the render with a clear message.
    for value in ("bogus", "Pod", ""):
        bad = render_helm({"clickhouse": {"backend": value}})
        check(
            bad.returncode != 0 and "clickhouse.backend must be" in bad.stderr,
            f"backend {value!r} fails the render",
        )
    bad = render_helm(
        {"clickhouse": {"backend": "external", "external": {"host": ""}}}
    )
    check(
        bad.returncode != 0
        and "clickhouse.external.host must be set" in bad.stderr,
        "external without clickhouse.external.host fails the render",
    )


def main() -> int:
    # The phalanx CLI render is the default (pod) backend.
    cli_text = render_phalanx()
    mirror = render_helm(None)
    check(
        mirror.returncode == 0 and mirror.stdout == cli_text,
        "helm template as phalanx runs it reproduces the phalanx CLI render",
    )
    pod = docs(cli_text)

    ext_run = render_helm({"clickhouse": {"backend": "external"}})
    check(ext_run.returncode == 0, "external backend renders")
    ext = docs(ext_run.stdout)

    check_both("pod", pod)
    check_both("external", ext)
    check_guard("pod", pod)
    check_guard("external", ext)
    check_external(pod, ext)
    check_overrides()

    out("")
    if failures:
        out(f"render_test: {len(failures)} FAILED")
        return 1
    out("render_test: all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
