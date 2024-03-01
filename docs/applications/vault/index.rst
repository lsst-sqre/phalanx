.. px-app:: vault

######################
vault — Secret Storage
######################

Vault provides the storage for secrets which are materialized into
Phalanx applications as Kubernetes Secrets.

It is simply the `Official Hashicorp Helm chart for Vault <https://github.com/hashicorp/vault-helm>`__ configured the way we require.

It is intended to run under Roundtable, and there should only be one production and one development instance per organization-with-its-own-secret-store.

The Vault Agent Injector is not enabled since we instead use the :doc:`Vault Secrets Operator <../vault-secrets-operator/index>`.

Vault is configured in HA mode with a public API endpoint accessible at https://vault.lsst.cloud, or https://vault-dev.lsst.cloud for the development instance.
TLS termination is done at the nginx ingress layer using a Let's Encrypt server certificate.
The UI is available at `vault.lsst.cloud <https://vault.lsst.cloud/ui>`__ for the production instance, and `vault-dev.lsst.cloud <https://vault-dev.lsst.cloud/ui>`__ for the development instance.

To directly manipulate the secrets stored in this Vault instance, use `lsstvaultutils <https://github.com/lsst-sqre/lsstvaultutils>`__ .
However, in normal operation, secrets will be managed via each application's ``secrets.yaml`` and manual interaction with Vault and its data will not be necessary.

Guides
======

.. toctree::
   :maxdepth: 2

   seal
   external
   migration
   upgrade
   values
