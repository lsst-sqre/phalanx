###############################
Sync secrets for an environment
###############################

To populate Vault with all of the necessary secrets for an environment named ``<environment>``, run:

.. code-block::

   phalanx secrets sync <environment>

The ``VAULT_TOKEN`` environment variable must be set to the Vault write token for this environment.
Add the ``--secrets`` command-line option or set ``OP_CONNECT_TOKEN`` if needed for your choice of a :ref:`static secrets source <admin-static-secrets>`.

This must be done before installing a Phalanx environment for the first time.
It can then be run again whenever the secrets for that environment change.

By default, this will leave any existing generated secrets set to their current values.
This is almost always what you want.
In the rare case where you are completely reinstalling an environment and want to invalidate all existing secrets (such as after a security breach), you can add the ``--regenerate`` flag to regenerate all static secrets.

.. warning::

   Using ``--regenerate`` will invalidate all user sessions, all user tokens, and other, possibly unanticipated, interactions with the existing cluster.
   It will also break most running Phalanx applications until their secrets have been recreated and they have been restarted.

   This should only be used when you also plan to empty the Gafaelfawr database and otherwise reset the environment to start fresh.

You may also add the ``--delete`` flag to remove any secrets from Vault that are no longer required for this environment.
This will keep your Vault tidy, but you should use this flag with caution if you have applications temporarily disabled or if you store static secrets directly in Vault and nowhere else.
It will delete anything that it thinks is not necessary, and recovering those secrets may be annoying.
