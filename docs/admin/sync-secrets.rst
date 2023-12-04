###############################
Sync secrets for an environment
###############################

Before syncing secrets for an environment, you should normally audit the secrets so that you know what will change.
See :doc:`audit-secrets`.

To populate Vault with all of the necessary secrets for an environment named ``<environment>``, run:

.. prompt:: bash

   phalanx secrets sync <environment>

The ``VAULT_TOKEN`` environment variable must be set to the Vault write token for this environment.
For SQuaRE-managed environments, you can get the write token from the ``Phalanx Vault write tokens`` item in the SQuaRE 1Password vault.

Add the ``--secrets`` command-line option or set ``OP_CONNECT_TOKEN`` if needed for your choice of a :ref:`static secrets source <admin-static-secrets>`.
For SQuaRE-managed deployments, the 1Password token for ``OP_CONNECT_TOKEN`` comes from the ``Phalanx 1Password tokens`` item in the SQuaRE 1Password vault.

This must be done before installing a Phalanx environment for the first time.
It can then be run again whenever the secrets for that environment change.

Deleting secrets
================

By default old secrets that are no longer required are deleted out of Vault.
To delete obsolete secrets, pass the ``--delete`` flag to :command:`phalanx secrets sync`.

This will keep your Vault tidy, but you should use this flag with caution if you have applications temporarily disabled or if you store static secrets directly in Vault and nowhere else.
This flag will delete anything that :command:`phalanx secrets sync` thinks is not used, and recovering those secrets may be annoying.

Regenerating secrets
====================

By default, :command:`phalanx secrets sync` will leave any existing generated secrets set to their current values.
This is almost always what you want.
In the rare case where you are completely reinstalling an environment and want to invalidate all existing secrets (such as after a security breach), you can add the ``--regenerate`` flag to regenerate all static secrets.

.. warning::

   Using ``--regenerate`` will invalidate all user sessions, all user tokens, and other, possibly unanticipated, interactions with the existing cluster.
   It will also break most running Phalanx applications until their secrets have been recreated and they have been restarted.

   This should only be used when you also plan to empty the Gafaelfawr database and otherwise reset the environment to start fresh.
