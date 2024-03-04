.. _secrets:

###########################
Secrets management overview
###########################

Phalanx is a public repository on GitHub, nevertheless application configurations generally require some secrets such as random numbers, certificates, or passwords.
This page explains how secrets are managed in Phalanx with Vault_, 1Password_, and `Vault Secrets Operator`_.

Vault
=====

Phalanx uses Vault to store the canonical source of all secrets for a Phalanx environment.
These secrets are then copied into Kubernetes ``Secret`` resources using :px-app:`vault-secrets-operator`.

Helm charts that need secrets use ``VaultSecret`` resources with the name matching the Secret_ resource to create.
Those ``VaultSecret`` resources are configured with the path in Vault to the secret.
That path, in turn, is configured in the Helm per-environment values files for those applications.

Most Rubin Science Platform installations use the Vault server at ``vault.lsst.cloud``.
This is currently managed using Roundtable_ but will eventually be managed using Phalanx itself.
This Vault server uses Rubin Observatory 1Password vaults as its ultimate source of secrets that cannot be randomly generated.

However, Phalanx does not require using any specific Vault server or any specific method of secrets or credential management in Vault.
As long as the correct secrets can be created in Vault and vault-secrets-operator can be configured to read those secrets, Phalanx can work with any Vault server.

1Password
=========

While Kubernetes and Argo CD do not look beyond Vault, Vault is not the source of truth for persistent secrets for Rubin Science Platform environments maintained by SQuaRE.
Secrets for external applications or which for whatever reason cannot be randomly regenerated when the environment is reinstalled are called *static secrets*.

There are several ways that static secrets can be managed (see :ref:`admin-static-secrets`).
SQuaRE uses 1Password for the static secrets for most environments that we manage.
For more details on this secrets management approach, see :ref:`admin-secrets-onepassword`.

For a step-by-step guide on adding a 1Password-based secret, see :doc:`/admin/add-new-secret`.
For updating an existing 1Password-based secret, see :doc:`/admin/update-a-secret`.
