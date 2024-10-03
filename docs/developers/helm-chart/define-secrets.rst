##############################
Define the application secrets
##############################

To allow Phalanx to manage and verify the secrets for an application, every secret that the application uses must be configured.
This configuration is used to generate secrets that can be randomly generated, copy secret values from an external source if appropriate, and ensure that all secrets required for the application are present in Vault.

If the application doesn't have any secrets, you can skip this step and continue to :doc:`add-application`.

If you have not already written a Helm chart for your application, do that first, following the instructions in either :doc:`create-new-chart` or :doc:`/developers/add-external-chart`.

.. _dev-secret-definition:

Create the secret definitions
=============================

Secrets for each application are specified by a file named :file:`secrets.yaml` at the top level of the application chart directory (at the same level as :file:`Chart.yaml`).

Applications can also define additional secrets used only in specific environments in a :file:`secrets-{environment}.yaml` file.
Those secrets are merged with the secrets defined in :file:`secrets.yaml` (and override those secrets if they have the same key).

These are YAML files.
The top-level keys are the names of each application secret.
This corresponds to the key within the ``Secret`` object that will be created in Kubernetes for the application.

The values are specifications of secrets.
The most important fields are ``description``, which should contain a human-readable description of the secret in reStructuredText, and ``generate``, which if set defines the rules to generate a random secret.

Secrets can also be copied from the secret for another application, to handle cases where two applications need to share a secret.
This is done with the ``copy`` directive.

Secrets may be conditional on specific Helm chart settings by using ``if``; in this case, the secret doesn't need to exist unless that Helm setting is true.
It's also possible for the generate or copy rules to be conditional, meaning that the secret is only generated or copied if some condition is set, and otherwise may be a static secret.

Secrets that contain newlines cannot be stored in 1Password as-is, since 1Password field values don't support newlines.
Mark these secrets by setting ``onepassword.encoded`` to ``true``, since they will be stored in 1Password with an additional layer of base64 encoding.
(You do not need to do this with :abbr:`GCP (Google Cloud Platform)` service account credentials.
Although their normal form contains newlines, they are encoded in JSON, so the newlines are not significant and may be stripped.)

For a full specification of the contents of this file, see :doc:`/developers/secrets-spec`.

Examples
--------

All of the following examples are single entries in the :file:`secrets.yaml` file for a service.

Here is the specification for static secret used by Argo CD to authenticate users with an external OpenID Connect server.
Since this contains no ``if`` or ``generate`` clauses, it must be provided as a static secret for all environments.

.. code-block:: yaml
   :caption: applications/argocd/secrets.yaml

   "dex.clientSecret":
     description: >-
       OAuth 2 or OpenID Connect client secret, used to authenticate to
       GitHub or Google as part of the authentication flow. This secret
       can be changed at any time.

The Gafaelfawr Redis password, used internally to authenticate to its dedicated Redis.
This is an example of a generated secret.
It is required for all environments, but will be generated automatically on first sync.

.. code-block:: yaml
   :caption: applications/gafaelfawr/secrets.yaml

   redis-password:
     description: >-
       Password used to authenticate Gafaelfawr to its internal Redis server,
       deployed as part of the same Argo CD application. This secret can be
       changed at any time, but both the Redis server and all Gafaelfawr
       deployments will then have to be restarted to pick up the new value.
     generate:
       type: password

Here is an example of a conditional static secret.
This is the password used by Gafaelfawr to authenticate to an external LDAP server.
It only needs to be provided if Gafaelfawr is configured to use an LDAP server, as determined by whether its values setting ``config.ldap.userDn`` is set to a true (non-empty) value.

.. code-block:: yaml
   :caption: applications/gafaelfawr/secrets.yaml

   ldap-password:
     description: >-
       Password to authenticate to the LDAP server via simple binds to
       retrieve user and group information. This password can be changed
       at any time.
     if: config.ldap.userDn

Here is an example of a secret that is always required but which is automatically generated in some environments but must be provided as a static secret in other environments.
This is the Gafaelfawr database password, which is a static secret when using an external database but a generated secret when using the in-cluster PostgreSQL server.

.. code-block:: yaml
   :caption: applications/gafaelfawr/secrets.yaml

   database-password:
     description: >-
       Password used to authenticate to the PostgreSQL database used to store
       Gafaelfawr data. This password may be changed at any time.
     generate:
       if: config.internalDatabase
       type: password

Here is an example of a secret that is copied from another application.
This is the matching definition of the Gafaelfawr database password in the in-cluster PostgreSQL server, which is copied from the Gafaelfawr application if Gafaelfawr is using the in-cluster database.

.. code-block:: yaml
   :caption: applications/postgres/secrets.yaml

   gafaelfawr_password:
     description: "Password for the Gafaelfawr database."
     if: gafaelfawr_db
     copy:
       application: gafaelfawr
       key: database-password

Finally, here is an example of a static secret that needs an additional layer of base64 encoding when stored in 1Password because its value contains newlines:

.. code-block:: yaml
   :caption: applications/nublado/secrets-idfdev.yaml

   "postgres-credentials.txt":
     description: >-
       PostgreSQL credentials in its pgpass format for the Butler database.
     onepassword:
       encoded: true

Define VaultSecret resources
============================

The Phalanx secrets tooling will ensure that the secret is in Vault, but you must still create or update a ``VaultSecret`` resource in your application's deployment, typically in its Helm chart, to tell `Vault Secrets Operator`_ how to create a ``Secret`` that your application can use.

A typical ``VaultSecret`` Helm template for an application looks like this (replace ``myapp`` with your application's name):

.. code-block:: yaml

   apiVersion: ricoberger.de/v1alpha1
   kind: VaultSecret
   metadata:
     name: "myapp"
     labels:
       {{- include "myapp.labels" . | nindent 4 }}
   spec:
     path: "{{ .Values.global.vaultSecretsPath }}/myapp"
     type: Opaque

The ``global.vaultSecretsPath`` setting will be injected into your application by Argo CD.

This Kubernetes resource will instruct `Vault Secrets Operator`_ to create a corresponding ``Secret`` resource containing the contents of the ``myapp`` vault secret located under the value of ``global.vaultSecretsPath``.
This ``Secret`` will have the same name and namespace as the ``VaultSecret`` object.

In some cases, you may not want to exactly copy the full Vault secret for the application.
Instead, you may want to only include some keys, create multiple secrets each with different subsets of the application's secret, add derived values to the secret because a third-party chart requires them, or perform other transformations.
This can be done using the templating features of `Vault Secrets Operator`_.
See the `vault-secrets-operator documentation <https://github.com/ricoberger/vault-secrets-operator#using-templated-secrets>`__ for more details.

.. note::

   The template syntax documented in the Vault Secrets Operator documentation assumes that secret keys will not contain hyphens (``-``), but we often use hyphens because they make for good human-readable names.
   To refer to a secret key that contains a hyphen in a Vault Secrets Operator template, use YAML and template syntax like the following:

   .. code-block:: yaml

      spec:
        templates:
          admin-password: >-
            {% index .Secrets "admin-password" %}

   The ``index`` function can retrieve secrets whose names are not valid identifiers (because, for instance, they contain a dash), and ``>-`` quoting avoids the conflict between two layers of quotes.
   This also works for other characters not allowed in identifiers, such as periods.

.. _dev-inject-secrets:

Inject the secrets into your application
========================================

Now that you have arranged for the creation of the ``Secret`` Kubernetes resource, you need to make those secrets available to your application.
There are two main ways to give a ``Deployment``, ``StatefulSet``, ``CronJob``, or other pod-creating resource access to secrets:

- `Set environment variables based on secrets <https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#define-container-environment-variables-using-secret-data>`__
- `Mount the secrets as files in the container <https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#create-a-pod-that-has-access-to-the-secret-data-through-a-volume>`__

Add the new secrets
===================

Adding secrets for a new application must be done by the environment administrator, since it requires write access to the Vault and possibly the static secret store for the environment.

Once you have defined the secrets for your new application, contact the administrator of that environment and provide the values of any static secrets that you are using.
They will then use one or more of the following processes:

- :doc:`/admin/add-new-secret`
- :doc:`/admin/update-a-secret`
- :doc:`/admin/sync-secrets`

Next steps
==========

- Check the validity of your newly-written chart: :doc:`check-chart`
- Add the Argo CD application to appropriate environments: :doc:`add-application`
