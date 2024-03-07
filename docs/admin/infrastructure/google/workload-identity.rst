########################
Set up workload identity
########################

All Kubernetes applications that need to access Google Cloud services will running in Google Kubernetes Engine should use `workload identity`_ to do so.
This allows applications running in Kubernetes pods to authenticate as Google service accounts without worrying about key management or separate secrets.

Configuring a Kubernetes application to use workload identity is documented at :doc:`/developers/helm-chart/workload-identity`.
Using this requires some configuration on the Google side, which for SQuaRE-managed environments we do via Terraform at https://github.com/lsst/idf_deploy.

Terminology
===========

Workload identity requires connecting two things that are both called service accounts, so it can be confusing.
It helps to be very precise about terminology.

Google service account
    A Google Cloud identity used by services (not, normally, humans).
    The Google service account exists outside of Kubernetes, is visible in the IAM portion of the Google console, and can be granted permissions to access arbitrary Google Cloud services.
    The goal of workload identity is to grant access to a Kubernetes pod to take actions as a Google service account.

    Google service accounts have a name that looks like an e-mail address and which contains the name of the Google project in which the service account lives.

Kubernetes service account
    A Kubernetes service account corresponds to a ``ServiceAccount`` resource.
    It is internal to a given Kubernetes cluster, and normally only grants access to Kubernetes resources and APIs.
    It cannot directly be used to access anything outside of that Kubernetes cluster.
    Normally, for permissions in Kubernetes, the service account is granted permissions using a ``Role`` and ``RoleBinding`` or a ``ClusterRole`` and ``ClusterRoleBinding``, but it can also be granted access to a Google service account using the mechanism discussed below.

    Kubernetes service accounts are associated with Kuberntes namespaces, and two service accounts with identical names can exist in differnet namespaces.
    Those service accounts are distinct and have entirely separate permissions.
    When referring to Kubernetes service accounts, it's therefore good practice to include the namespace (so ``gafaelfawr/gafaelfawr-operator``, for example, which is the ``gafaelfawr-operator`` service account in the ``gafaelfawr`` namespace.

    Every Kubernetes pod runs with the credentials of some Kubernetes service account, although the workload inside the pod may or may not have access to those credentials.
    If none is specified, a Kubernetes service account named ``default`` is used.

Project
    Google Cloud services are divided into projects.
    All objects in Google Cloud live in a specific project.
    For service accounts, the project they live in is part of the service account name, immediately after the ``@`` sign.
    A Google service account in one project can be (and often is) granted access to objects in other projects.

Role
    Google service accounts by default don't have permission to do anything significant.
    To grant a Google service account permissions, grant it a *role*.
    The role always has a *target resource*, which limits where those permissions are applicable.
    This resource can be a specific object in Google (such as a Cloud Storage bucket), in which case the role permissions apply only to that object, or it can be a Google Cloud project, in which case the permissions apply to any relevant object in that Google Cloud project.
    As mentioned, the resource can be in a different project than the service account.

Overview of workload identity
=============================

The goal of the workload identity configuration is to allow a Kubernetes pod to obtain Google service account credentials, which it can then use to make calls directly to Google Cloud services.
That involves the following steps:

#. Create a Google service account for use by an application.
#. Assign appropriate permissions to that Google service account for the Google Cloud services that it will access.
#. Configure the Kubernetes pod to run with a specific Kubernetes service account.
   This part is done in :doc:`/developers/helm-chart/workload-identity`.
#. Tell Google Kubernetes Engine what Google service account the Kubernetes service account should be mapped to.
   This part is done in :doc:`/developers/helm-chart/workload-identity`.
#. Tell Google Cloud IAM what Kubernetes service accounts are allowed to take actions as that Google service account.

All five steps are necessary.
Once all are complete, the Kubernetes pod will be able to obtain temporary credentials as the Google service account and then use those credentials to make API calls to Google Cloud services.
The Google Cloud libraries will automatically recognize that workload identity is in use without any further configuration.

Configuration steps
===================

1. Create a Google service account
----------------------------------

In the :file:`main.tf` part of the Terraform configuration, create the Google service account for the application with Terraform such as the following::

   resource "google_service_account" "<application>_sa" {
     account_id   = "<application>"
     display_name = "<name>"
     description  = "Terraform-managed service account for <name>"
     project      = module.project_factory.project_id
   }

Replace ``<application>`` with the name of the Phalanx application (all lowercase).
Use dashes if there are dashes in the Phalanx application name except on the first line, where dashes should be replaced with underscores.
Replace ``<name>`` with the human-readable name of the application.

If the service account is instead intended only for Cloud SQL access, see the separate :file:`cloudsql/main.tf` configuration file instead.
There will be a ``service_accounts`` configuration block.
You can add an additional service account to the list in the ``names`` parameter.

2. Assign permissions to the service account
--------------------------------------------

Use the regular Google Cloud IAM resources to assign appropriate permissions to the service account.
For example, code like this grants access to a Google Coud Storage bucket::

   resource "google_storage_bucket_iam_member" "<application>_sa_storage" {
     bucket = module.storage_bucket.name
     role   = "roles/storage.objectUser"
     member = "serviceAccount:<application>@${module.project_factory.project_id}.iam.gserviceaccount.com"
   }

As above, replace ``<application>`` with the Phalanx application name.

This Terraform configuration should go into the configuration for the project that contains the resource to which you are granting access, **not** the project in which the Google service account is defined, if those two projects are different.
In this case, you will have to replace ``${module.project_factory.project_id}`` with the actual Google project name rather than letting Terraform do it for you.

As a special case, if the service needs to be able to generate signed URLs, it must be granted permissions to impersonate itself.
This is a very strange-looking permission since the identity and the target are both the same.
It is required because workload identity authentication normally does not give the client an X.509 private key, but the private key is required to create self-signed URLs.
This permission allows the client to request a temporary X.509 private key that it can use for URL signing.

.. code-block::

   resource "google_service_account_iam_member" "<application>_sa_iam" {
     service_account_id = google_service_account.<application>_sa.name
     role               = "roles/iam.serviceAccountTokenCreator"
     member             = "serviceAccount:${google_service_account.<application>_sa.email}"
   }

This configuration must go into the same Terraform configuration file as the creation of the service account.

.. note::

   The Google service account name referenced throughout this documentation is the email-address-like name shown in the Google console and also used by the :command:`gcloud` command-line tool.
   Terraform stores this the ``.email`` attribute of the service account and uses ``.name`` for an internal identifier suitable for ``service_account_id``.
   Be careful not to confuse those when writing Terraform policy.

If the Google service account will only be used for Cloud SQL access, no further permission grants are required, since granting that role will be done by the ``service_accounts`` block you edited in step 1.

3. Map the Kubernetes service account to the Google service account
-------------------------------------------------------------------

To tell Google which Kubernetes service accounts can act as a Google service account, you must grant the special ``roles/iam.workloadIdentityUser`` role on the Google service account to a special service account name that Google uses to represent a Kubernetes service account.
The Terraform code to do that looks like this::

   resource "google_service_account_iam_member" "<application>_sa_wi" {
     service_account_id = google_service_account.<application>_sa.name
     role               = "roles/iam.workloadIdentityUser"
     member             = "serviceAccount:${module.project_factory.project_id}.svc.id.goog[<namespace>/<service-account>]"
   }

Replace ``<application>`` with the application name as above, ``<namespace>`` with the Kubernetes namespace of the application and ``<service-account>`` with the Kubernetes service account name.
By convention, we use Kubernetes service account names that match the application name for applications with only one Kubernetes service account, but some complex applications may have more than one and may use a more specific name.

If the application has multiple Kubernetes service accounts that should map to the same Google service account, add multiple blocks like the above, one for each service account.

This Terraform configuration should go into the same Terraform file as the creation of the service account.

4. Provide the Google service account names to the developer
------------------------------------------------------------

Once these changes have been merged and deployed with Terraform, provide the Google service account names to the application developer.
Each Phalanx environment should have a separate corresponding Google service account, and hence a separate Google service account name, which looks like an email address.
Usually the left-hand part before the ``@`` will be the same for every environment but the project name immediately after the ``@`` will differ.
These service account names are then configured in the :file:`values-{environment}.yaml` files for the application.
