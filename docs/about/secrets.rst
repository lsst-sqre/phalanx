.. _secrets:

###########################
Secrets management overview
###########################

Phalanx is a public repository on GitHub, nevertheless application configurations generally require some secrets such as random numbers, certificates, or passwords.
This page explains how secrets are managed in Phalanx with Vault, 1Password, and Vault Secrets Operator.

Vault
=====

Argo CD allows all application configurations to be checked into Git and deployed from that repository.
However, many application configurations require some secrets such as random numbers, certificates, or passwords.
These obviously cannot be committed to a public repository.
We instead use `Vault`_ to store secrets and then materialize them in Kubernetes using :px-app:`vault-secrets-operator`.

.. _Vault: https://www.vaultproject.io/

Helm charts that need secrets use ``VaultSecret`` resources with the name matching the Secret_ resource to create.
Those ``VaultSecret`` resources are configured with the path in Vault to the secret.
That path, in turn, is configured in the Helm per-environment values files for those applications.

Most Rubin Science Platform installations use the Vault server at ``vault.lsst.codes``, which is managed using Roundtable_.

Each installation environment has its own root path in that Vault server.
The path is formatted as ``k8s_operator/<fqdn>`` where ``<fqdn>`` is the domain name of that environment.
When the environment is bootstrapped, it is given a Kubernetes secret with the Vault token required to read that path of Vault.
See :dmtn:`122` for more information about that Vault instance and its naming conventions.

1Password
=========

While Kubernetes and Argo CD do not look beyond Vault, Vault is not the source of truth for persistent secrets for Rubin Science Platform environments maintained by SQuaRE.
Secrets for external applications or which for whatever reason cannot be randomly regenerated when the environment is reinstalled are stored in `1Password`_.

Inside 1Password, there is a vault named ``RSP-Vault`` that contains all of the persistent secrets.
Each secret is stored in either a Login or a Secure Note object.
Inside that object, there must be a key named ``generate_secrets_key`` whose value is two words separated by a space.
The first word is the application's name and the second is the name of that secret among the secrets for that application.
There may also be one or more keys named ``environment``.
Its values are the domain names of the environments to which that specific secret applies.
If ``environment`` is missing, that 1Password object provides a default for the given ``generate_secrets_key`` key, which will be used if there is no other object with the same key and a matching environment.

These 1Password objects are used by the `generate_secrets.py script <https://github.com/lsst-sqre/phalanx/blob/master/installer/generate_secrets.py>`__ as part of the installation process to retrieve the persistent secrets.
Ephemeral secrets that can be reset when the environment is reinstalled are generated during the installation process.
`update_secrets.sh <https://github.com/lsst-sqre/phalanx/blob/master/installer/update_secrets.sh>`__ uses the ``onepassword_uuid`` setting in `/environments/values.yaml <https://github.com/lsst-sqre/phalanx/blob/master/environments/values.yaml>`__ to locate the appropriate 1Password vault.

For a step-by-step guide on adding a 1Password-based secret, see :doc:`/developers/add-a-onepassword-secret`.
For updating an existing 1Password-based secret, see :doc:`/developers/update-a-onepassword-secret`.
