##################
Seal configuration
##################

A Vault database is "sealed" by encrypting the stored data with an encryption key, which in turn is encrypted with a master key.
In a default Vault installation, the master key is then split with Shamir secret sharing and a quorum of key fragments is required to manually unseal the Vault each time the Vault server is restarted.
This is a poor design for high availability and for Kubernetes management, so we instead use an "auto-unseal" configuration.

Auto-unsealing works by using a Google KMS key as the master key.
That KMS key is stored internally by Google and cannot be retrieved or downloaded, but an application can request that data be encrypted or decrypted with that key.
Vault has KMS decrypt the encryption key on startup and then uses that to unseal the Vault database.
The Vault server uses a Google service account with permission on the relevant key ring to authenticate to KMS to perform this operation.

In auto-unseal mode, there is still a manual key, but this key is called a "recovery key" and cannot be used to unseal the database.
It is, however, still needed for certain operations, such as seal key migration.

The recovery key for the Vault is kept in 1Password.

.. _change-seal:

##################
Changing seal keys
##################

It is possible to change the key used to seal Vault (if, for instance, Vault needs to be migrated to another GCP project), but it's not well-documented and is moderately complicated.
Here are the steps:

#. Add ``disabled = "true"`` to the ``seal`` configuration stanza in ``values-<env>.yaml``.
   At this point your seal configuration should point to the old project/location/keyring/key.
#. Change ``vault.server.ha.replicas`` to 1 in ``values-<env>.yaml``.
#. Push the changes and sync Argo CD to remove the other running Vault containers.
   Argo CD may complain about synchronizing the affinity configuration; this is harmless and can be ignored.
#. Relaunch the ``vault-0`` pod by deleting it and letting Kubernetes recreate it.
#. Get the recovery key from 1Password.
#. ``kubectl exec --namespace=vault -ti vault-0 -- vault operator unseal -migrate`` and enter the recovery key.
   This will disable auto-unseal and convert the unseal recovery key to be a regular unseal key using Shamir.
   Vault is no longer using the KMS key at this point.
#. Change the KMS ``seal`` configuration stanza in ``values.yaml`` to point to the new KMS project, location, keyring, and key that you want to use.
   Remove ``disabled = "true"`` from the ``seal`` configuration.
   Push this change and sync Argo CD.
#. Relaunch the ``vault-0`` pod by deleting it and letting Kubernetes recreate it.
#. ``kubectl exec --namespace=vault -ti vault-0 -- vault operator unseal -migrate`` and enter the recovery key.
   This will reseal Vault using the KMS key and convert the unseal key you have been using back to being a recovery key.
   Even though you are resealing Vault, you should use the ``operator unseal`` command.
#. Change ``vault.server.ha.replicas`` back to 3 in ``values.yaml``, push, and synchronize Argo CD to start the remaining Vault pods.
