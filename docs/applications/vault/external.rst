######################
External configuration
######################

This deployment is currently only tested on GCP.

Vault resources are stored in `the IDF deployment terraform configuration <https://github.com/lsst/idf_deploy/tree/main/environment/deployments/roundtable>`__.
All resources are in a single GCP project.
The summary of these resources is as follows:

#. The service account for the Vault service, whose name is ``vault-server``::

       resource "google_service_account" "vault_server_sa" {
         account_id   = "vault-server"
         display_name = "Vault Server"
         description  = "Terraform-managed service account for Vault server"
         project      = module.project_factory.project_id
       }

#. A KMS keyring named ``vault-server`` holding a single key named ``vault-seal``.
   This has owners, encrypters, and decrypters all set to a single-item list whose value is the ``vault-server`` service account for that project::

       module "kms" {
	 source         = "../../../modules/kms"
	 project_id     = module.project_factory.project_id
	 location       = "us-central1"
	 keyring        = "vault-server"
	 keys           = ["vault-seal"]
	 set_owners_for = ["vault-seal"]
	 decrypters     = ["serviceAccount:vault-server@${module.project_factory.project_id}.iam.gserviceaccount.com"]
	 encrypters     = ["serviceAccount:vault-server@${module.project_factory.project_id}.iam.gserviceaccount.com"]
	 owners         = ["serviceAccount:vault-server@${module.project_factory.project_id}.iam.gserviceaccount.com"]
       }

#. A storage bucket for the Vault data.
   This bucket has lifecycle rules keeping three versions of each item it contains::

       module "storage_bucket" {
	 source        = "../../../modules/bucket"
	 project_id    = module.project_factory.project_id
	 storage_class = "REGIONAL"
	 location      = "us-central1"
	 suffix_name   = [var.vault_server_bucket_suffix]
	 prefix_name   = "rubin"
	 versioning = {
	   (var.vault_server_bucket_suffix) = true
	 }
	 lifecycle_rules = [
	   {
	     action = {
	       type = "Delete"
	     }
	     condition = {
	       num_newer_versions = 3
	     }
	   }
	 ]
	 force_destroy = {
	   (var.vault_server_bucket_suffix) = false
	 }
	 labels = {
	   environment = var.environment
	   application = "vault"
	 }
       }


#. A backup storage bucket.
   This one's lifecycle keeps twenty versions of each item::

       module "storage_bucket_b" {
	 source        = "../../../modules/bucket"
	 project_id    = module.project_factory.project_id
	 storage_class = "REGIONAL"
	 location      = "us-central1"
	 suffix_name   = ["${var.vault_server_bucket_suffix}-backup"]
	 prefix_name   = "rubin"
	 versioning = {
	   "${var.vault_server_bucket_suffix}-backup" = true
	 }
	 lifecycle_rules = [
	   {
	     action = {
	       type = "Delete"
	     }
	     condition = {
	       num_newer_versions = "20"
	     }
	   }
	 ]
	 force_destroy = {
	   "${var.vault_server_bucket_suffix}-backup" = false
	 }
	 labels = {
	   environment = var.environment
	   application = "vault"
	 }
       }

#. A Workload Identity IAM member binding the service account to ``<project-id>>.svc.id.goog[vault/vault]``.
   That is, the GCP service account will be bound to the ``vault`` service account in the ``vault`` Kubernetes namespace::

       resource "google_project_iam_member" "vault_server_sa_wi" {
	 project = module.project_factory.project_id
	 role    = "roles/iam.workloadIdentityUser"
	 member  = "serviceAccount:${module.project_factory.project_id}.svc.id.goog[vault/vault]"
       }


   The Kubernetes resource is, in turn, annotated with ``iam.gke.io/gcp-service-account: "vault-server@<project-id>.gserviceaccount.com"``.
   This provides the two-way linkage allowing the Vault Kubernetes application to use Workload Identity and therefore avoid needing to store any persistent credentials.

#. IAM members binding the roles ``Cloud KMS Viewer`` and ``Cloud KMS CryptoKey Encrypter/Decrypter`` to the service account::

       resource "google_project_iam_member" "vault_server_viewer_sa" {
	 project = module.project_factory.project_id
	 role    = "roles/cloudkms.viewer"
	 member  = "serviceAccount:vault-server@${module.project_factory.project_id}.iam.gserviceaccount.com"
       }

       resource "google_project_iam_member" "vault_server_cryptokey_sa" {
	 project = module.project_factory.project_id
	 role    = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
	 member  = "serviceAccount:vault-server@${module.project_factory.project_id}.iam.gserviceaccount.com"
       }

#. Storage bucket IAM members binding the service account to the role ``storage.objectUser`` for the Vault storage bucket and to ``storage.admin`` for the backup bucket::

       resource "google_storage_bucket_iam_member" "vault_server_storage_sa" {
	 bucket  = module.storage_bucket.name
	 role    = "roles/storage.objectUser"
	 member  = "serviceAccount:vault-server@${module.project_factory.project_id}.iam.gserviceaccount.com"
       }

       resource "google_storage_bucket_iam_member" "vault_server_storage_backup_sa" {
	 bucket  = module.storage_bucket_b.name
	 role    = "roles/storage.admin"
	 member  = "serviceAccount:vault-server@${module.project_factory.project_id}.iam.gserviceaccount.com"
       }


#. A hidden service account for the backup storage transfer job.
   The storage transfer job creates this automatically, but does not give it sufficient permissions for backups to work, so we need to explicitly specify it in order to grant those permissions::

       data "google_storage_transfer_project_service_account" "vault_backup_transfer_sa" {
	 project = module.project_factory.project_id
       }

       resource "google_storage_bucket_iam_member" "vault_server_storage_transfer_source_sa" {
	 bucket  = module.storage_bucket.name
	 role    = "roles/storage.objectViewer"
	 member  = "serviceAccount:${data.google_storage_transfer_project_service_account.vault_backup_transfer_sa.email}"
       }

#. IAM bindings for the transfer service account to grant ``storage.ObjectViewer`` and ``storage.legacyBucketReader`` to the source bucket and ``storage.admin``, ``storage.legacyBucketReader``, and ``storage.legacyBucketWriter`` to the destination bucket::

       resource "google_storage_bucket_iam_member" "vault_server_storage_transfer_source_sa" {
	 bucket  = module.storage_bucket.name
	 role    = "roles/storage.objectViewer"
	 member  = "serviceAccount:${data.google_storage_transfer_project_service_account.vault_backup_transfer_sa.email}"
       }

       resource "google_storage_bucket_iam_member" "vault_server_storage_transfer_source_sa_r" {
	 bucket  = module.storage_bucket.name
	 role    = "roles/storage.legacyBucketReader"
	 member  = "serviceAccount:${data.google_storage_transfer_project_service_account.vault_backup_transfer_sa.email}"
       }

       resource "google_storage_bucket_iam_member" "vault_server_storage_transfer_sink_sa" {
	 bucket  = module.storage_bucket_b.name
	 role    = "roles/storage.legacyBucketWriter"
	 member  = "serviceAccount:${data.google_storage_transfer_project_service_account.vault_backup_transfer_sa.email}"
       }

       resource "google_storage_bucket_iam_member" "vault_server_storage_transfer_sink_sa_r" {
	 bucket  = module.storage_bucket_b.name
	 role    = "roles/storage.legacyBucketReader"
	 member  = "serviceAccount:${data.google_storage_transfer_project_service_account.vault_backup_transfer_sa.email}"
       }

#. The transfer job itself, copying from the Vault server bucket to the backup bucket every night at 10 AM UTC (2 AM or 3 AM Project Time).
   The job has a dependency on the transfer service account bindings, because otherwise a race condition will prevent it from being created correctly via Terraform::

       resource "google_storage_transfer_job" "vault_server_storage_backup" {
	 description = "Nightly backup of Vault Server storage"
	 project     = module.project_factory.project_id
	 transfer_spec {
	   gcs_data_source {
	     bucket_name = module.storage_bucket.name
	   }
	   gcs_data_sink {
	     bucket_name = module.storage_bucket_b.name
	   }
	 }
	 schedule {
	   schedule_start_date {
	     year  = 2024
	     month = 1
	     day   = 1
	   }
	   start_time_of_day { // UTC: 2 AM Pacific Standard Time
	     hours   = 10
	     minutes = 0
	     seconds = 0
	     nanos   = 0
	   }
	 }
	 depends_on = [google_storage_bucket_iam_member.vault_server_storage_transfer_source_sa,google_storage_bucket_iam_member.vault_server_storage_transfer_sink_sa,google_storage_bucket_iam_member.vault_server_storage_transfer_source_sa_r,google_storage_bucket_iam_member.vault_server_storage_transfer_sink_sa_r]
       }


All of the configuration except for the GCP S3 bucket names is found directly in `main.tf <https://github.com/lsst/idf_deploy/blob/main/environment/deployments/roundtable/main.tf>`__.
The bucket names, each of which must be globally unique, are found in environment-specific variable files, e.g. `production.tfvars <https://github.com/lsst/idf_deploy/blob/main/environment/deployments/roundtable/env/production.tfvars>`__
