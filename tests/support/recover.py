"""Helpers for testing cluster recovery pre-flight checks."""

from typing import Any
from unittest.mock import Mock

from google.cloud.compute_v1beta import Address, Firewall
from google.cloud.container_v1 import Cluster, PrivateClusterConfig

from phalanx.factory import Factory

from ..support.command import MockCommand
from ..support.data import PhalanxData
from ..support.google_cloud import MockGoogleCloudClients
from ..support.helm import MockHelmCommand
from ..support.vault import MockVaultClient

__all__ = ["MockRecover"]


class MockRecover:
    """Helpers to mock the universe for cluster recovery tests."""

    def __init__(
        self,
        data: PhalanxData,
        factory: Factory,
        mock_helm: MockHelmCommand,
        mock_vault: MockVaultClient,
        mock_argocd: MockCommand,
        mock_kubectl: MockCommand,
        mock_google_cloud: MockGoogleCloudClients,
    ) -> None:
        self.data = data
        self.factory = factory
        self.helm = mock_helm
        self.vault = mock_vault
        self.argocd = mock_argocd
        self.kubectl = mock_kubectl
        self.google_cloud = mock_google_cloud

    def mock_connect_check(
        self, *, fail_source: bool = False, fail_destination: bool = False
    ) -> None:
        """Mock stuff for success or failure of the kubectl connect check."""
        error = Exception("Can't connect")
        source_call = error if fail_source else "Some source version"
        destination_call = error if fail_destination else "Some dest version"

        self.kubectl.expect_capture(("version",), source_call)
        self.kubectl.expect_capture(("version",), destination_call)

    def mock_static_ip_check(self, *, fail: bool = False) -> None:
        """Mock stuff for success or failure of the static ip check."""
        if fail:
            filename = "kubectl/service-list-wrong-ip.json"
        else:
            filename = "kubectl/service-list.json"

        self.kubectl.expect_capture(
            args=(
                "get",
                "Service",
                "--field-selector",
                "spec.type=LoadBalancer",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
            response=self.data.read_text(filename),
        )

        self.add_side_effects(
            self.google_cloud.addresses.list,
            [Address(address="35.225.112.77")],
        )

    def mock_firewall_check(
        self, *, fail_ips: bool = False, fail_tags: bool = False
    ) -> None:
        """Mock stuff for success or failure of the firewall check."""
        source_cidr = "1.1.1.1/1"
        destination_cidr = "2.2.2.2/2"

        ips = [source_cidr] if fail_ips else [source_cidr, destination_cidr]

        if fail_tags:
            tags = [
                "gke-some-source-cluster",
            ]
        else:
            tags = [
                "gke-some-source-cluster",
                "gke-some-destination-cluster",
            ]

        self.add_side_effects(
            self.google_cloud.firewalls.get,
            Firewall(
                source_ranges=ips,
                target_tags=tags,
            ),
        )

        self.add_side_effects(
            self.google_cloud.gke.get_cluster,
            Cluster(
                private_cluster_config=PrivateClusterConfig(
                    master_ipv4_cidr_block=source_cidr
                )
            ),
            Cluster(
                private_cluster_config=PrivateClusterConfig(
                    master_ipv4_cidr_block=destination_cidr
                )
            ),
        )

    def mock_source_sync_check(
        self, environment_name: str, *, fail: bool = False
    ) -> None:
        """Mock stuff for success or failure of the ArgoCD sync check."""
        # Vault login
        config_storage = self.factory.create_config_storage()
        environment = config_storage.load_environment(environment_name)
        self.vault.load_test_data(
            self.data, environment.vault_path_prefix, environment_name
        )

        if fail:
            filename = "argocd/application-list.json"
        else:
            filename = "argocd/application-list-all-synced.json"

        # ArgoCD list applications
        args = (
            "app",
            "list",
            "-l",
            "argocd.argoproj.io/instance=science-platform",
            "--port-forward",
            "--port-forward-namespace",
            "argocd",
            "-o",
            "json",
        )
        output = self.data.read_text(filename)
        self.argocd.expect_capture(args=args, response=output)

    def mock_happy_restore(self) -> None:
        """Mock the universe for a successful cluster restore."""
        # Set source cluster volumes to retain
        self.kubectl.expect_capture(
            args=("get", "PersistentVolume", "-o", "json"),
            response=self.data.read_text("kubectl/persistent-volumes.json"),
        )

        # Release Service LoadBalancerIP's
        self.kubectl.expect_capture(
            args=(
                "get",
                "Service",
                "--field-selector",
                "spec.type=LoadBalancer",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
            response=self.data.read_text("kubectl/service-list.json"),
        )

        responses = (
            "kubectl/service-ingress-nginx-controller-cluster-ip-with-finalizers.json",
            "kubectl/service-ingress-nginx-controller-cluster-ip-without-finalizers.json",
            "kubectl/service-ingress-nginx-controller-released.json",
        )
        for response in responses:
            self.kubectl.expect_capture(
                args=(
                    "get",
                    "Service",
                    "ingress-nginx-controller",
                    "--namespace",
                    "ingress-nginx",
                    "-o",
                    "json",
                ),
                response=self.data.read_text(response),
            )

        # Suspend cronjobs
        self.kubectl.expect_capture(
            args=(
                "get",
                "CronJob",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
            response=self.data.read_text("kubectl/cronjob-list.json"),
        )

        # Scale down workloads
        self.kubectl.expect_capture(
            args=(
                "get",
                "Deployment",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
            response=self.data.read_text("kubectl/deployment-list.json"),
        )

        # Scale down workloads
        self.kubectl.expect_capture(
            args=(
                "get",
                "StatefulSet",
                "-l",
                "argocd.argoproj.io/instance",
                "-o",
                "json",
                "--all-namespaces",
            ),
            response=self.data.read_text("kubectl/statefulset-list.json"),
        )

        # Set destination cluster volumes to retain
        self.kubectl.expect_capture(
            args=("get", "PersistentVolume", "-o", "json"),
            response=self.data.read_text("kubectl/persistent-volumes.json"),
        )

        # Get the sasquatch kafka cluster id
        overrides = self.data.read_text(
            "kubectl/get-kafka-cluster-id-overrides"
        ).strip()
        self.kubectl.expect_capture(
            args=(
                "run",
                "tmp",
                "-itq",
                "--rm",
                "--restart",
                "Never",
                "--image",
                "foo",
                "--overrides",
                overrides,
                "--namespace",
                "sasquatch",
            ),
            response="some-cluster-id",
        )

        # ArgoCD: wait for app statuses to be set
        self.argocd.expect_capture(
            args=(
                "app",
                "list",
                "-l",
                "argocd.argoproj.io/instance=science-platform",
                "--port-forward",
                "--port-forward-namespace",
                "argocd",
                "-o",
                "json",
            ),
            response=self.data.read_text("argocd/application-list.json"),
        )

        # ArgoCD: sync specific kinds of resources
        for _ in (
            "VaultSecret",
            "KafkaUser",
            "KafkaTopic",
            "KafkaAccess",
            "Kafka",
            "Certificate",
            "KafkaNodePool",
            "ServiceAccount",
            "ConfigMap",
        ):
            self.argocd.expect_capture(
                args=(
                    "app",
                    "list",
                    "-l",
                    "argocd.argoproj.io/instance=science-platform",
                    "--port-forward",
                    "--port-forward-namespace",
                    "argocd",
                    "-o",
                    "json",
                ),
                response=self.data.read_text("argocd/application-list.json"),
            )

        # Wait for Kafka to be ready
        self.kubectl.expect_capture(
            args=(
                "get",
                "Kafka",
                "sasquatch",
                "--namespace",
                "sasquatch",
                "-o",
                "json",
            ),
            response=self.data.read_text("kubectl/kafka.json"),
        )

    def add_side_effects(self, mock: Mock, *side_effects: Any) -> None:
        """Add a side effect to the existing list of side effects for mock.

        Parameters
        ----------
        mock
            The mock object to add side effects to
        side_effects
            The side effects to add
        """
        current = mock.side_effect or []
        mock.side_effect = [*current, *side_effects]

    def assert_run_calls(self, prefix: str) -> None:
        """Assert "run" calls to all command mocks."""
        kubectl_calls = self.kubectl.mock.run.call_args_list
        argocd_calls = self.argocd.mock.run.call_args_list
        helm_calls = self.helm.call_args_list

        path = f"recover/{prefix}-kubectl-calls"
        self.data.assert_calls_match(kubectl_calls, path)

        path = f"recover/{prefix}-argocd-calls"
        self.data.assert_calls_match(argocd_calls, path)

        path = f"recover/{prefix}-helm-calls"
        self.data.assert_json_matches(helm_calls, path)
