"""Constants for the Phalanx support code.

Things that arguably could be configurable but haven't yet been made into
actual configuration options.
"""

from datetime import timedelta

__all__ = [
    "HELM_DOCLINK_ANNOTATION",
    "ONEPASSWORD_ENCODED_WARNING",
    "PREVIOUS_EXTERNAL_TRAFFIC_POLICY_ANNOTATION",
    "PREVIOUS_LOAD_BALANCER_IP_ANNOTATION",
    "PULL_SECRET_DESCRIPTION",
    "VAULT_APPROLE_SECRET_TEMPLATE",
    "VAULT_TOKEN_SECRET_TEMPLATE",
    "VAULT_WRITE_TOKEN_LIFETIME",
    "VAULT_WRITE_TOKEN_WARNING_LIFETIME",
]

HELM_DOCLINK_ANNOTATION = "phalanx.lsst.io/docs"
"""Annotation in :file:`Chart.yaml` for application documentation links."""

ONEPASSWORD_ENCODED_WARNING = (
    "If you store this secret in a 1Password item, encode it with base64"
    " first."
)
"""Warning to add to secrets that must be encoded in 1Password."""

PULL_SECRET_DESCRIPTION = (
    "Pull secrets for Docker registries. Each key under registries is the name"
    " of a Docker registry that needs a pull secret. The value should have two"
    " keys, username and password, that provide the HTTP Basic Auth"
    " credentials for that registry."
)
"""Description to put in the static secrets YAML file for ``pull-secret``."""

VAULT_APPROLE_SECRET_TEMPLATE = """\
apiVersion: v1
kind: Secret
metadata:
  name: {name}
  namespace: vault-secrets-operator
data:
  VAULT_ROLE_ID: {role_id}
  VAULT_SECRET_ID: {secret_id}
type: Opaque
"""
"""Template for a ``Secret`` containing AppRole credentials."""

VAULT_TOKEN_SECRET_TEMPLATE = """\
apiVersion: v1
kind: Secret
metadata:
  name: {name}
  namespace: vault-secrets-operator
data:
  VAULT_TOKEN: {token}
type: Opaque
"""
"""Template for a ``Secret`` containing token credentials."""

VAULT_WRITE_TOKEN_LIFETIME = "3650d"
"""Default lifetime to set for Vault write tokens."""

VAULT_WRITE_TOKEN_WARNING_LIFETIME = timedelta(days=7)
"""Remaining lifetime at which to warn that a token is about to expire."""

PREVIOUS_REPLICA_COUNT_ANNOTATION = "phalanx.lsst.org/previous-replica-count"
"""Annotation that holds the original number of replicas.

This annotation will be set when we do an explicit scale down during a recovery
process.
"""

PREVIOUS_LOAD_BALANCER_IP_ANNOTATION = (
    "phalanx.lsst.org/previous-load-balancer-ip"
)
"""Annotation that holds the original loadBalancerIP value for a Service.

This annotation will be set when we recover an existing Phalanx cluster to a
new cluster.
"""

PREVIOUS_EXTERNAL_TRAFFIC_POLICY_ANNOTATION = (
    "phalanx.lsst.org/previous-external-traffic-policy"
)
"""Annotation that holds the original Service externalTrafficPolicy value.

When we convert a LoadBalancer service to a ClusterIP service, then back to a
LoadBalancer service, spec.externalTrafficPolicy always gets set to "Cluster",
even if it was set to "Local" originally.
"""

GKE_LOAD_BALANCER_SERVICE_FINALIZERS = [
    "service.kubernetes.io/load-balancer-cleanup",
    "gke.networking.io/l4-netlb-v1",
]
"""Finalizers on a GKE Service resource when the service has an ingress."""
