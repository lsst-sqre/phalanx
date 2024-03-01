"""Test integration with Sphinx Jinja templating."""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from phalanx.constants import HELM_DOCLINK_ANNOTATION
from phalanx.docs.jinja import build_jinja_contexts
from phalanx.factory import Factory
from phalanx.models.environments import IdentityProvider

from ..support.data import (
    phalanx_test_path,
    read_output_data,
    read_output_json,
)


def test_build_jinja_contexts(factory: Factory) -> None:
    config_dir = phalanx_test_path()
    cwd = Path.cwd()

    # build_jinja_contexts expects to be run from a top-level subdirectory of
    # the configuration root, since that's what Sphinx does.
    os.chdir(str(config_dir / "environments"))

    try:
        contexts = build_jinja_contexts()

        # Test the basic structure of the contexts.
        idfdev = contexts["idfdev"]["env"]
        minikube = contexts["minikube"]["env"]
        for application in idfdev.applications:
            assert application.name in contexts
            assert contexts[application.name]["app"] == application
            assert contexts[application.name]["envs"]["idfdev"] == idfdev
            assert contexts[application.name]["envs"]["minikube"] == minikube

        # Check the additional environment information we gather.
        assert idfdev.name == "idfdev"
        assert idfdev.fqdn == "data-dev.lsst.cloud"
        assert idfdev.argocd_url == "https://data-dev.lsst.cloud/argo-cd"
        assert idfdev.identity_provider == IdentityProvider.CILOGON
        assert idfdev.gcp.project_id == "science-platform-dev-7696"
        assert idfdev.gcp.region == "us-central1"
        assert idfdev.gcp.cluster_name == "science-platform"
        assert minikube.name == "minikube"
        assert minikube.fqdn == "minikube.lsst.cloud"
        assert minikube.argocd_url is None
        assert minikube.identity_provider == IdentityProvider.GITHUB
        assert minikube.gcp is None

        # Check some of the more complex data.
        expected = read_output_data("idfdev", "argocd-rbac-rst")
        assert "\n".join(idfdev.argocd_rbac_csv) == expected.strip()
        scopes = {s.scope: s.groups_as_rst() for s in idfdev.gafaelfawr_scopes}
        assert scopes == read_output_json("idfdev", "gafaelfawr-scopes")
        scopes = {
            s.scope: s.groups_as_rst() for s in minikube.gafaelfawr_scopes
        }
        assert scopes == read_output_json("minikube", "gafaelfawr-scopes")

        # Check some of the additional application data that isn't used by the
        # command-line tests, only by the documentation.
        gafaelfawr = contexts["gafaelfawr"]["app"]
        chart_path = (
            config_dir
            / "applications"
            / "infrastructure"
            / "gafaelfawr"
            / "Chart.yaml"
        )
        with chart_path.open("r") as fh:
            chart = yaml.safe_load(fh)
        assert gafaelfawr.chart == chart
        assert gafaelfawr.homepage == chart["home"]
        assert gafaelfawr.source_urls == chart["sources"]
        docs = yaml.safe_load(chart["annotations"][HELM_DOCLINK_ANNOTATION])
        assert [d.model_dump() for d in gafaelfawr.doc_links] == docs
        expected = (
            "`DMTN-234: RSP identity management design"
            " <https://dmtn-234.lsst.io/>`__"
        )
        assert gafaelfawr.doc_links[0].to_rst() == expected
        assert gafaelfawr.active_environments == ["idfdev", "minikube"]

        # Check that we have a context for the tap application even though
        # it's not enabled by any environment.
        assert contexts["tap"]
        assert contexts["tap"]["app"].active_environments == []
    finally:
        os.chdir(str(cwd))
