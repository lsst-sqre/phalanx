#####################################################
Updating a secret stored in 1Password and VaultSecret
#####################################################

Secrets that are stored in 1Password are synchronized into Vault using the `installer/generate_secrets.py <https://github.com/lsst-sqre/phalanx/blob/master/installer/generate_secrets.py>`__ script.
Once they are in Vault, they are accessible to the Vault Secrets Operator, which responds to creation of any ``VaultSecret`` resources in Kubernetes by grabbing the current value of the secret data in Vault.

The Vault Secrets Operator doesn't independently detect if there are changes to data in Vault, though.
It only provides a snapshot of the data in Vault at the time the ``VaultSecret`` was created.

So, if you want to make any changes to a ``VaultSecret``'s data, you'll need to:

1. Make the changes in 1Password
2. Run the `installer/update_secrets.sh <https://github.com/lsst-sqre/phalanx/blob/master/installer/update_secrets.sh>`__ script, as described in :doc:`/service-guide/add-a-onepassword-secret`.
3. Delete the ``VaultSecret`` in the ArgoCD UI.
4. Sync your application in ArgoCD, recreating the ``VaultSecret``, and triggering the Vault Secrets Operator to incorporate your changes.


Deleting the ``VaultSecret``
========================

You can delete the ``VaultSecret`` by first navigating to your Application in ArgoCD.

Find the ``VaultSecret`` resource in your application, and click on it.
You should see a "delete" button in the top right of the dialog that pops up.

Click "delete", and go through with it; a "foreground delete" is sufficient.
Be sure not to navigate away from this page until you see the resource get deleted in the UI, since ArgoCD will delete it and the underlying Secret with background calls.

Once done, you can Sync your application in order to recreate the VaultSecret.
