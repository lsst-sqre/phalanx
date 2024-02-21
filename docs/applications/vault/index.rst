.. px-app:: vault

###########################
Vault — Secret Storage
###########################

Vault provides the storage for secrets which are materialized into
Phalanx applications as Kubernetes Secrets.

It is simply the `Official Hashicorp Helm chart for Vault <https://github.com/hashicorp/vault-helm>`__ configured the way we require.

It is intended to run under Roundtable, and there should only be one production and one development instance per organization-with-its-own-secret-store.

vault-kms-creds
===============

Note that the application, when used with the Google Cloud Storage backend, has a resource, not documented in ``secrets.yaml``, which is a manually created secret called ``vault-kms-creds`` with a single key, ``credentials.json``.  This holds the specification of the service account that can access the vault storage buckets, which must have access to the roles ``Cloud KMS Viewer`` and ``Cloud KMS CryptoKey Encrypter/Decrypter``.  This secret cannot use ``secrets.yaml`` because it is the secret needed to bootstrap the whole ``vault-secrets-operator`` system on which the standard Phalanx secrets management system depends.

.. jinja:: vault
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
