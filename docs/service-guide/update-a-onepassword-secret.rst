#####################################################
Updating a secret stored in 1Password and VaultSecret
#####################################################

Secrets that are stored in 1Password are synchronized into Vault using the `installer/generate_secrets.py <https://github.com/lsst-sqre/phalanx/blob/master/installer/generate_secrets.py>`__ script.
Once they are in Vault, they are accessible to the Vault Secrets Operator, which responds to creation of any ``VaultSecret`` resources in Kubernetes by grabbing the current value of the secret data in Vault.

The Vault Secrets Operator reconciles any changes as well by comparing Vault's state with that of any ``VaultSecret``s every 60 seconds.
This reconciliation process can also take a bit of time; the net result is that you can expect changes to be reflected after a few minutes.

.. note::

   Note for operators: This automatic reconciliation is not enabled by default.
   It is explicitly turned on by setting the ``vault.reconciliationTime`` key in the Helm chart, which needs to be done in every deployed environment of the Vault Secrets Operator.

So, if you want to make any changes to a ``VaultSecret``'s data, you'll need to:

1. Make the changes in 1Password
2. Run the `installer/update_secrets.sh <https://github.com/lsst-sqre/phalanx/blob/master/installer/update_secrets.sh>`__ script, as described in :doc:`/service-guide/add-a-onepassword-secret`.
3. Wait a few minutes for automatic reconciliation


Forcing reconciliation
======================

If automatic reconciliation doesn't seem to be working, you can force it to take place by deleting the ``Secret`` that is associated with the ``VaultSecret``.
The ``Secret`` will have the same name as its parent ``VaultSecret``.
Once you delete the ``Secret``, the Vault Secrets Operator should detect the deletion and recreate it quickly.
