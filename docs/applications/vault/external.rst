######################
External configuration
######################

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
