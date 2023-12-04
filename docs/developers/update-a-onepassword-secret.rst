#####################################
Updating a secret stored in 1Password
#####################################

If you are adding a new secret, start by adding the new secret definition to :file:`secrets.yaml` or :file:`secrets-{environment}.yaml` in that application's chart.
See :ref:`dev-secret-definition` for more details.

For environments with static secrets stored in 1Password, updating them requires access to the 1Password Vault used by that enviroment.
This may have to be done for you by an environment administrator.

#. Open the 1Password Vault for the environment whose secret you want to update.
   You can find the name of this vault in the ``onepassword.vaultTitle`` key in the :file:`environments/values-{environment}.yaml` file for your environment.

#. Find the 1Password Vault item named for your application.
   Be aware that when multiple applications use the same static secret, one of them is defined as the "owner" and the other applications use ``copy`` directives in their :file:`secrets.yaml` files to copy the secret from the "owning" application.
   It's the item for the owning application that you need to update.

#. Replace the value of the secret with a new value.

#. Sync secrets for that environment.
   See :doc:`/admin/sync-secrets`.

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
