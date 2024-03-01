###############
Vault Migration
###############

If you want to migrate a Vault deployment from one GCP project and Kubernetes cluster to another, do the following:

#. Create the resources required for the new Vault server in the new GCP project.
   If you are not using Terraform via `the IDF deployment terraform configuration <https://github.com/https://github.com/lsst/idf_deploy/tree/main/environment/deployments/roundtable>`__ consult that repository to understand what resources you will need and create them by hand.
#. Grant the new service account access to the KMS keyring and key used for unsealing in the old GCP project.
   This is necessary to be able to do a seal migration later.
   See `this StackOverflow answer <https://stackoverflow.com/questions/49214127/can-you-share-google-cloud-kms-keys-across-projects-with-service-roles>`__ for how to grant access.
   The new service account must have Cloud KMS Viewer and Cloud KMS Encrypter/Decrypter permissions on the old KMS keyring and key.
#. Copy the data from the old GCS bucket to the new GCS bucket using a GCS transfer.
#. Configure the new vault to point to the KMS keyring and key in the old project.
#. Do as directed in :ref:`change-seal` to switch from the old seal key in KMS in the old GCP project to the new seal key in the new GCP project.
#. Change DNS to point the Vault server name (generally ``vault.lsst.cloud``) to point to the new installation.
#. Remove the permissions to the old KMS keyring and key from the new service account.
