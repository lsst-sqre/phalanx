###############################
Sync secrets for an environment
###############################

Phalanx uses :px-app:`vault-secrets-operator` to create Kubernetes ``Secret`` resources from ``VaultSecret`` resources and entries in Vault.
It requires every Phalanx application with secrets have its own entry in Vault whose keys and values collect all secrets used by that application.
Some secrets therefore have to be duplicated between applications, and others can be automatically generated if missing.
This process of copying and generating secrets as needed is called syncing secrets.

Syncing secrets must be done before installing a Phalanx environment for the first time, and then every time the secrets for that environment change.
Even if the environment stores static secrets in Vault directly, secrets will still need to be synced periodically to handle the copied and generated secrets also stored in Vault.

Syncing secrets
===============

.. warning::

   Before syncing secrets for an environment, you should normally audit the secrets so that you know what will change.
   See :doc:`audit-secrets`.

To populate Vault with all of the necessary secrets for an environment named ``<environment>``, run:

.. tab-set::

   .. tab-item:: General

      .. prompt:: bash

         phalanx secrets sync <environment>

      Add the ``--secrets`` command-line option or set ``OP_CONNECT_TOKEN`` if needed for your choice of a :ref:`static secrets source <admin-static-secrets>`.
      For SQuaRE-managed deployments, the 1Password token for ``OP_CONNECT_TOKEN`` comes from the ``Phalanx 1Password tokens`` item in the SQuaRE 1Password vault.

      If you did not store the Vault write token for your environment with the static secrets, the ``VAULT_TOKEN`` environment variable must be set to the Vault write token for this environment.
      For SQuaRE-managed environments, you can get the write token from the ``Phalanx Vault write tokens`` item in the SQuaRE 1Password vault.

   .. tab-item:: SQuaRE-managed environments (1Password)

      .. prompt:: bash

         op run --env-file="op/<environment>.env" -- phalanx secrets sync <environment>

      See :doc:`op-run-phalanx-cli` for details on :command:`op run`.

Only secrets for the named environment will be affected.
No changes will be made outside of the configured secrets path for that environment.

Deleting secrets
================

By default, old secrets that are no longer required are not deleted out of Vault.
To delete obsolete secrets, pass the ``--delete`` flag to :command:`phalanx secrets sync`.

This will keep your Vault tidy, but you should use this flag with caution if you have applications temporarily disabled or if you store static secrets directly in Vault and nowhere else.
This flag will delete anything that :command:`phalanx secrets sync` thinks is not used, and recovering those secrets may be annoying.

Regenerating secrets
====================

By default, :command:`phalanx secrets sync` will leave any existing generated secrets set to their current values.
This is almost always what you want.

In the rare case where you are completely reinstalling an environment and want to invalidate all existing secrets (such as after a security breach), you can add the ``--regenerate`` flag to regenerate all non-static secrets.

.. warning::

   Using ``--regenerate`` will invalidate all user sessions, all user tokens, and other, possibly unanticipated, interactions with the existing cluster.
   It will also break most running Phalanx applications until their Kubernetes ``Secret`` resources have been recreated and they have been restarted.

   This should only be used when you also plan to empty the Gafaelfawr database and otherwise reset the environment to start fresh.
