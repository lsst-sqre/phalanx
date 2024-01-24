#####################################
Managing GCP resources with Terraform
#####################################

All SQuaRE-managed Google Cloud Platform projects use Terraform to manage all GCP resources outside of Kubernetes.
These include CLoud SQL databases used by Phalanx applications, Google Firestore for UID and GID assignment, service accounts used with workload identity for authenticated access to Google services, and so forth.

The Terraform configuration for all SQuaRE-managed projects and most other Rubin Observatory GCP projects is maintained in https://github.com/lsst/idf_deploy.
Changes to this repository are automatically applied to the relevant Google Cloud Platform project when the pull request has been reviewed and merged.
