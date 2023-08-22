.. _secrets:

###########################
Secrets management overview
###########################

Phalanx is a public repository on GitHub, nevertheless application configurations generally require some secrets such as random numbers, certificates, or passwords.
This page explains how secrets are managed in Phalanx with Vault_, 1Password_, and `Vault Secrets Operator`_.

.. warning::

   We are in the midst of a migration to a new method for secrets management.
   You may therefore encounter multiple instructions for how to manage secrets, and may have to make changes in multiple locations to keep the different mechanisms in sync.
   Once the migration is complete, the Phalanx command-line tool will be used for all secrets management.

Vault
=====

Phalanx uses Vault to store the canonical source of all secrets for a Phalanx environment.
These secrets are then copied into Kubernetes ``Secret`` resources using :px-app:`vault-secrets-operator`.

Helm charts that need secrets use ``VaultSecret`` resources with the name matching the Secret_ resource to create.
Those ``VaultSecret`` resources are configured with the path in Vault to the secret.
That path, in turn, is configured in the Helm per-environment values files for those applications.

Most Rubin Science Platform installations use the Vault server at ``vault.lsst.codes``.
This is currently managed using Roundtable_ but will eventually be managed using Phalanx itself.
This Vault server uses Rubin Observatory 1Password vaults as its ultimate source of secrets that cannot be randomly generated.

However, Phalanx does not require using any specific Vault server or any specific method of secrets or credential management in Vault.
As long as the correct secrets can be created in Vault and vault-secrets-operator can be configured to read those secrets, Phalanx can work with any Vault server.

1Password
=========

While Kubernetes and Argo CD do not look beyond Vault, Vault is not the source of truth for persistent secrets for Rubin Science Platform environments maintained by SQuaRE.
Secrets for external applications or which for whatever reason cannot be randomly regenerated when the environment is reinstalled are stored in 1Password_.

.. note::

   The 1Password layout described here is the old layout and is being changed as part of the secrets migration.
   For details about the new layout, not yet deployed, see :sqr:`079`.

Inside 1Password, there is a vault named ``RSP-Vault`` that contains all of the persistent secrets.
Each secret is stored in either a Login or a Secure Note object.
Inside that object, there must be a key named ``generate_secrets_key`` whose value is two words separated by a space.
The first word is the application's name and the second is the name of that secret among the secrets for that application.
There may also be one or more keys named ``environment``.
Its values are the domain names of the environments to which that specific secret applies.
If ``environment`` is missing, that 1Password object provides a default for the given ``generate_secrets_key`` key, which will be used if there is no other object with the same key and a matching environment.

These 1Password objects are used by the `generate_secrets.py script <https://github.com/lsst-sqre/phalanx/blob/main/installer/generate_secrets.py>`__ as part of the installation process to retrieve the persistent secrets.
Ephemeral secrets that can be reset when the environment is reinstalled are generated during the installation process.
`update_secrets.sh <https://github.com/lsst-sqre/phalanx/blob/main/installer/update_secrets.sh>`__ uses the ``onepassword_uuid`` setting in `/environments/values.yaml <https://github.com/lsst-sqre/phalanx/blob/main/environments/values.yaml>`__ to locate the appropriate 1Password vault.

For a step-by-step guide on adding a 1Password-based secret, see :ref:`dev-add-onepassword`.
For updating an existing 1Password-based secret, see :doc:`/developers/update-a-onepassword-secret`.
