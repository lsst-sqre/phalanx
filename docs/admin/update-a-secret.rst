######################
Update a static secret
######################

The process for updating a static secret depends on how static secrets are stored for that environment.
Since it requires write access to the underlying secret store, updates must be done by an enviroment administrator.

Static secrets in a YAML file
=============================

If the environment stores static secrets in a secure YAML file, the environment administrator should update that file with the newly-required static secrets.
Then, sync the secrets into Vault following the instructions in :doc:`/admin/sync-secrets`.

Static secrets stored directly in Vault
=======================================

If the environment stores static secrets directly in Vault, the environment administrator should change the static secret directly in Vault.
Be aware that when multiple applications use the same static secret, one of them is defined as the "owner" and the other applications use ``copy`` directives in their :file:`secrets.yaml` files to copy the secret from the "owning" application.
In this case, the static secret must be updated separately for every copy.

When the static secrets are stored directly in Vault, no separate sync step is required.

Static secrets stored in 1Password
==================================

#. Open the 1Password Vault for the environment whose secret you want to update.
   You can find the name of this vault in the ``onepassword.vaultTitle`` key in the :file:`environments/values-{environment}.yaml` file for your environment.

#. Find the 1Password Vault item named for your application.
   Be aware that when multiple applications use the same static secret, one of them is defined as the "owner" and the other applications use ``copy`` directives in their :file:`secrets.yaml` files to copy the secret from the "owning" application.
   It's the item for the owning application that you need to update.

#. Replace the value of the secret with a new value.

#. Sync secrets for that environment.
   See :doc:`sync-secrets`.

If the same secret is used in multiple environments, these steps must be done for every environment.

When do secrets change in Kubernetes?
=====================================

Once the secrets have been synced, `Vault Secrets Operator`_ reconciles any changes as well by comparing Vault's state with that of any ``VaultSecret`` resources every 60 seconds.
This reconciliation process can take some time of time, so you may not see changes reflected until several minutes have passed.

.. note::

   This automatic reconciliation is not enabled by default in the upstream configuration.
   It is explicitly turned on by setting the ``vault.reconciliationTime`` key in the Helm chart, which Phalanx sets by default.

If automatic reconciliation doesn't seem to be working or is taking longer than you want to wait, you can force it to take place by deleting the ``Secret`` that is associated with the ``VaultSecret``.
The ``Secret`` will have the same name as its parent ``VaultSecret``.
Once you delete the ``Secret``, Vault Secrets Operator should detect the deletion and recreate it quickly.
