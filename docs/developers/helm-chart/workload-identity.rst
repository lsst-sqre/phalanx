###########################################
Tying service accounts to workload identity
###########################################

If your application will access Google Cloud services when running on Google Kubernetes Engine, it should use `workload identity`_ to authenticate to those services.
This allows applications running in Kubernetes pods to authenticate as Google service accounts without worrying about key management or separate secrets.

Set up Kubernetes service account
=================================

To use workload identity, your application must run as a specific, named Kubernetes service account.
Do not use the ``default`` service account created for each namespace.

Start by creating a Kubernetes service account for your application:

.. code-block:: yaml
   :caption: serviceaccount.yaml

   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: <application>
     labels:
       {{- include "<application>.labels" . | nindent 4 }}
     annotations:
       iam.gke.io/gcp-service-account: {{ required "serviceAccount must be set to a valid Google service account" .Values.serviceAccount | quote }}

Replace ``<application>`` with the name of your application.

Note the annotation.
This tells Kubernetes which Google service account your application will be authenticating as.
Once the Google service account has been created, you will add the appropriate service account name for each environment to your :file:`values-{environment}.yaml` files.

Configure the Pod
=================

Then, in your Deployment_, and any other Kubernetes resource that creates pods that need to talk to Google services, configure Kubernetes to run the pod with that service account:

.. code-block:: yaml
   :caption: deployment.yaml

   template:
     spec:
       serviceAccountName: <application>

Also ensure that ``automountServiceAccountToken`` is set to true or not set.
If the application uses the Google Cloud libraries, no further application configuration is required.
The Google Cloud libraries will automatically recognize that workload identity is in use and will make the necessary API calls to get Google Cloud credentials.

Making workload identity conditional
====================================

These examples configure the application to use workload identity unconditionally.
If the application may be deployed either under Google Kubernetes Engine or in other Kubernetes deployments, you will want to make workload identity conditional.
Do that by adding ``{{- if .Values.serviceAccount }}`` or similar conditional blocks around both the ``ServiceAccount`` resource and around the ``serviceAccountName`` setting.

Configuring the service account name
====================================

The above examples use ``serviceAccountName`` as the :file:`values.yaml` setting.
If the service account is only for CloudSQL, normal practice is to name the setting ``cloudsql.serviceAccountName`` and make workload identity conditional on whether ``cloudsql.enabled`` is true.
If your application uses workload identity for other purposes, you can either use a top-level values setting as shown here, or put the setting wherever seems most appropriate (associated with one specific part of your application, for instance).

For each environment where you want to use workload identity, the Phalanx environment administrator must create a Google service account for your application and associate it with the namespace and Kubernetes service account name used by your application.
See :doc:`/admin/infrastructure/google/workload-identity`.
They will then tell you what service account name to use for each environment.

Multiple service accounts
=========================

This is a simple configuration for an application that uses only one service account.
If you have a more complex application that also needs Kubernetes permissions, you may need multiple service accounts with more specific names than just the name of your overall application.
For an example of a more complicated configuration with multiple service accounts, see `giftless's Helm chart <https://github.com/lsst-sqre/phalanx/tree/main/applications/giftless>`__.
