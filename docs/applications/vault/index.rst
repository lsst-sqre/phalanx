.. px-app:: vault

###########################
Vault — Secret Storage
###########################

Vault provides the storage for secrets which are materialized into
Phalanx applications as Kubernetes Secrets.

It is simply the `Official Hashicorp Helm chart for Vault <https://github.com/hashicorp/vault-helm>`__ configured the way we require.

It is intended to run under Roundtable, and there should only be one production and one development instance per organization-with-its-own-secret-store.

The Vault Agent Injector is not enabled since we instead use the :doc:`Vault Secrets Operator <../vault-secrets-operator/index>`.

Vault is configured in HA mode with a public API endpoint accessible at https://vault.lsst.cloud, or https://vault-dev.lsst.cloud for the development instance.
TLS termination is done at the nginx ingress layer using a Let's Encrypt server certificate.
The UI is available at `vault.lsst.cloud <https://vault.lsst.cloud/ui>`__ for the production instance, and `vault-dev.lsst.cloud <https://vault-dev.lsst.cloud/ui>`__ for the development instance.

To directly manipulate the secrets stored in this Vault instance, use `lsstvaultutils <https://github.com/lsst-sqre/lsstvaultutils>`__ .
However, in normal operation, secrets will be managed via each application's ``secrets.yaml`` and manual interaction with Vault and its data will not be necessary.

.. rubric:: Seal configuration

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

.. rubric:: Changing seal keys

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

.. _external:

.. rubric:: External configuration

This deployment is currently only tested on GCP.

Vault resources are stored in `the IDF deployment terraform configuration <https://github.com/lsst/idf_deploy/tree/main/environment/deployments/roundtable>`__.
All resources are in a single GCP project.
The summary of these resources is as follows:

#. The service account for the Vault service, whose name is ``vault-server``.
#. A KMS keyring named ``vault-server`` holding a single key named ``vault-seal``.
   This has owners, encrypters, and decrypters all set to a single-item list whose value is the ``vault-server`` service account for that project.
#. A storage bucket for the Vault data.
   This bucket has lifecycle rules keeping three versions of each item it contains.
#. A backup storage bucket.
   This one's lifecycle keeps twenty versions of each item.
#. A Workload Identity IAM member binding the service account to ``<project-id>>.svc.id.goog[vault/vault]``.
   That is, the GCP service account will be bound to the ``vault`` service account in the ``vault`` Kubernetes namespace.
   The Kubernetes resource is, in turn, annotated with ``iam.gke.io/gcp-service-account: "vault-server@<project-id>.gserviceaccount.com"``.
   This provides the two-way linkage allowing the Vault Kubernetes application to use Workload Identity and therefore avoid needing to store any persistent credentials.
#. IAM members binding the roles ``Cloud KMS Viewer`` and ``Cloud KMS CryptoKey Encrypter/Decrypter`` to the service account.
#. Storage bucket IAM members binding the service account to the role ``storage.objectUser`` for the Vault storage bucket and to ``storage.admin`` for the backup bucket.
#. A hidden service account for the backup storage transfer job.
   The storage transfer job creates this automatically, but does not give it sufficient permissions for backups to work, so we need to explicitly specify it in order to grant those permissions.
#. IAM bindings for the transfer service account to grant ``storage.ObjectViewer`` and ``storage.legacyBucketReader`` to the source bucket and ``storage.admin``, ``storage.legacyBucketReader``, and ``storage.legacyBucketWriter`` to the destination bucket.
#. The transfer job itself, copying from the Vault server bucket to the backup bucket every night at 10 AM UTC (2 AM or 3 AM Project Time).
   The job has a dependency on the transfer service account bindings, because otherwise a race condition will prevent it from being created correctly via Terraform.

All of the configuration except for the GCP S3 bucket names is found directly in `main.tf <https://github.com/lsst/idf_deploy/blob/main/environment/deployments/roundtable/main.tf>`__.
The bucket names, each of which must be globally unique, are found in environment-specific variable files, e.g. `production.tfvars <https://github.com/lsst/idf_deploy/blob/main/environment/deployments/roundtable/env/production.tfvars>`__

.. rubric:: Migrating Vault

If you want to migrate a Vault deployment from one GCP project and Kubernetes cluster to another, do the following:

#. Create the resources required for the new Vault server in the new GCP project.
   If you are not using Terraform via `the IDF deployment terraform configuration <https://github.com/https://github.com/lsst/idf_deploy/tree/main/environment/deployments/roundtable>`__ consult that repository to understand what resources you will need and create them by hand.
#. Grant the new service account access to the KMS keyring and key used for unsealing in the old GCP project.
   This is necessary to be able to do a seal migration later.
   See `this StackOverflow answer <https://stackoverflow.com/questions/49214127/can-you-share-google-cloud-kms-keys-across-projects-with-service-roles>`__ for how to grant access.
   The new service account must have Cloud KMS Viewer and Cloud KMS Encrypter/Decrypter permissions on the old KMS keyring and key.
#. Copy the data from the old GCS bucket to the new GCS bucket using a GCS transfer.
#. Configure the new vault to point to the KMS keyring and key in the old project.
#. Perform a `seal migration <change-seal_>`_ to switch from the old seal key in KMS in the old GCP project to the new seal key in the new GCP project.
#. Change DNS to point the Vault server name (generally ``vault.lsst.cloud``) to point to the new installation.
#. Remove the permissions to the old KMS keyring and key from the new service account.

.. rubric:: Changing Vault configuration

When making configuration changes, be aware that Argo CD will not detect a change to the configuration and automatically relaunch the ``vault-*`` pods.
You will need to delete the pods and let Kubernetes recreate them in order to pick up changes to the configuration.

If you change the number of HA replicas, Argo CD will fail to fully synchronize the configuration because the ``PodDisruptionBudget`` resource cannot be updated.
Argo CD will show an error saying that a resource failed to synchronize.
To fix this problem, delete the ``PodDisruptionBudget`` resource in Argo CD and then resynchronize the ``vault`` app, and then Argo CD will be happy.

.. rubric:: Upgrading Vault

**WARNING: THIS SECTION MAY NO LONGER BE ACCURATE**

**REVISIT AFTER PERFORMING AN UPGRADE OF THE PHALANX-HOSTED VAULT**

Unlike many applications managed by Argo CD, upgrading Vault requires manual intervention.

The Vault Helm chart is monitored by WhiteSource Renovate and can be upgraded via the normal pull requests that tool creates.
It will not change the version of the Vault software itself.
When merging an update, Argo CD will get confused about the upgrade status of Vault.
Fixing this will require the manual intervention explained below.
It's good practice to check if Vault itself has an update each time the Vault Helm chart is updated.

To upgrade Vault itself, first change the pinned version in the ``server.image.tag`` setting in `/deployments/vault/values.yaml <https://github.com/lsst-sqre/roundtable/blob/master/deployments/vault/values.yaml>`__.
Then, after that change is merged and Argo CD has applied the changes in Kubernetes, follow the `Vault upgrade instructions <https://developer.hashicorp.com/vault/docs/platform/k8s/helm/run#upgrading-vault-servers>`__.
You can skip the ``helm upgrade`` step, since Argo CD has already made the equivalent change.
Where those instructions say to delete a pod, deleting it through Argo CD works correctly.
You don't need to resort to ``kubectl``.
Kubernetes will not automatically upgrade the servers because the Vault ``StatefulSet`` uses ``OnDelete`` as the update mechanism.

After the upgrade is complete, you will notice that Argo CD thinks a deployment is in progress and will show the application as **Progressing** rather than **Healthy**.
This is due to an `Argo CD bug <https://github.com/argoproj/argo-cd/issues/1881>`__.
To work around that bug:

#. Open the Argo CD dashboard and locate the ``StatefulSet``.
   You will see two or more ``ControllerRevision`` resources with increasing versions, and three ``Pod`` resources.
   Check all the ``Pod`` resources and confirm they're running the latest revision.
   (This should be the end result of following the above-linked upgrade instructions.)
#. Delete the unused ``ControllerRevision`` objects using Argo CD, leaving only the latest that matches the revision the pods are running.
#. Delete one of the stand-by pods and let Kubernetes recreate it.
   See the Vault upgrade instructions above for how to identify which pods are stand-by.

This should clear the erroneous **Progressing** status in Argo CD.

.. jinja:: vault
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
