##############################
Define the application secrets
##############################

To allow Phalanx to manage and verify the secrets for an application, every secret that the application uses must be configured.
This configuration is used to generate secrets that can be randomly generated, copy secret values from an external source if appropriate, and ensure that all secrets required for the application are present in Vault.

If the application doesn't have any secrets, you can skip this step and continue to :doc:`add-application`.

If you have not already written a Helm chart for your application, do that first, following the instructions in either :doc:`write-a-helm-chart` or :doc:`add-external-chart`.

Create the secret definitions
=============================

.. warning::

   All secrets should be defined using these files, but they are not yet used by default.
   Currently, the Phalanx installer uses :ref:`secret-definition-legacy`.
   Work is currently underway to switch from that mechanism to the new Phalanx command-line tool, which uses these definitions and automates the population of Vault.

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
(You do not need to do this with GCE service account credentials.
Although their normal form contains newlines, they are encoded in JSON, so the newlines are not significant and may be stripped.)

For a full specification of the contents of this file, see :doc:`secrets-spec`.

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

.. _secret-definition-legacy:

Create the secret generation rules (legacy)
===========================================

Currently, the Vault secrets for an environment are created using the `installer/generate_secrets.py script <https://github.com/lsst-sqre/phalanx/blob/main/installer/generate_secrets.py>`__.
That Python script can handle both static secrets that the installer needs to retrieve from 1Password or prompt for, and dynamic secrets that can be generated automatically via the ``SecretGenerator`` class.
Every application secret must have corresponding code in :file:`generate_secrets.py` to either generate it or prompt for it (which retrieves it from 1Password for SQuaRE-managed environments).

This script is used in conjunction with the `installer/update_secrets.sh script <https://github.com/lsst-sqre/phalanx/blob/main/installer/update_secrets.sh>`__ to populate the Vault secrets for a Phalanx environment.

Since this mechanism is currently being replaced with a new set of tooling, it is not documented here in detail.
Adding new secrets to this mechanism will require reading the source and following the pattern used by other applications.

Define VaultSecret resources
============================

Once a secret is in Vault, you need to create or update a ``VaultSecret`` resource in your application's deployment (typically in its Helm chart).
See :doc:`write-a-helm-chart` for more details on creating a Helm chart for an application.

A typical ``VaultSecret`` Helm template for an application looks like this (replace ``myapp`` with your application's name):

.. code-block:: yaml

   apiVersion: ricoberger.de/v1alpha1
   kind: VaultSecret
   metadata:
     name: {{ include "myapp.fullname" . }}
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
This can be done using the templating features of vault-secrets-operator.
See the `vault-secrets-operator documentation <https://github.com/ricoberger/vault-secrets-operator#using-templated-secrets>`__ for more details.

.. _dev-add-onepassword:

Create static secrets in 1Password (current)
============================================

.. note::

   This section only applies to Phalanx environments run by SQuaRE, which use 1Password as the backing store for static secrets, or environments run by other teams that choose to use 1Password.
   Using 1Password is not required by Phalanx.
   Static secrets can instead be stored directly in Vault or provided via other ways.
   Developers for those environments can skip this section.

For SQuaRE-run Phalanx environments, static secrets for applications are stored in a 1Password vault before being automatically synced to the Vault service.
Such secrets are things for external cloud services where we don't automatically provision accounts and password.
When we manually create such a secret, we store it in 1Password.

.. note::

   This document only covers creating a 1Password-backed secret for the first time for an application.
   If you want to update a secret, either by adding new 1Password secrets or by changing their secret values, you should follow the instructions in :doc:`/developers/update-a-onepassword-secret`.

.. warning::

   This process will be replaced with a new 1Password approach that uses separate vaults per environment.
   See :sqr:`079` for details.
   This documentation will be updated once that transition is complete.

1. Open the 1Password vault
---------------------------

In one password, access the **LSST IT** 1Password team and open the vault named ``RSP-Vault``.
Items in this vault are synced into Kubernetes ``Secret`` resources.

2. Create a secret note
-----------------------

Each item in a Kubernetes ``Secret`` corresponds to either the contents of a secure note or the password field of a login item in 1Password.
(Many 1Password items can combined into a single Kubernetes ``Secret`` in :file:`generate_secrets.py`.)

- The title of the 1Password item should be formatted as:

  .. code-block:: text

     {{application}} {{env}} {{description}}

  This format is a convention and isn't tied into the automation.
  The ``env`` can be omitted if the secret applies to all environments.

- Add the secret:

  - For a secure note, set the note's **contents** to the secret value.
  - For a login item, set the **password field** to the secret value.

- Add a metadata field labeled ``generate_secrets_key``. The value of that field is formatted as:

  .. code-block:: text

     {{application}} {{secret name}}

  This field provides part of a Vault path for the secret value, which in turn is used by :px-app:`vault-secrets-operator` resources to create Kubernetes secrets.

- Add a metadata field labeled ``environment``. The value of that field should be the **hostname** of the RSP environment that this secret applies to (e.g. ``data.lsst.cloud``, not the Phalanx name ``idfprod``).

  If the secret applies to multiple environments, add additional ``environment`` metadata fields for each environment.

  If the secret applies to **all** environments, omit the ``environment`` field altogether.

3. Sync 1Password items into Vault
----------------------------------

Once an application's secrets are stored in 1Password and :file:`generate_secrets.py` has been updated, you need to sync them into Vault.

First, set the ``OP_CONNECT_TOKEN`` environment variable to the access token for the SQuaRE 1Password Connect service.
This is stored in the SQuaRE 1Password vault under the item named ``SQuaRE Integration Access Token: Argo``.

Open Phalanx's ``installer/`` directory:

.. code-block:: sh

   cd installer

Install the Python dependencies (using a virtual environment is ideal):

.. code-block:: sh

   pip install -r requirements.txt

To sync the secrets for a single environment, run:

.. code-block:: sh

   ./update_secrets.sh {{hostname}}

For example:

.. code-block:: sh

   ./update_secrets.sh idf-dev.lsst.cloud

To sync multiple environments at once:

.. code-block:: sh

   ./update_all_secrets.sh

Create static secrets in 1Password (new)
========================================

.. warning::

   This section only applies to Phalanx environments run by SQuaRE that have been converted to the new 1Password setup that is currently under development.
   Most SQuaRE environments should continue to use the instructions in :ref:`dev-add-onepassword`.

For SQuaRE-run Phalanx environments, static secrets for applications are stored in a 1Password vault before being automatically synced to the Vault service.
Such secrets are things for external cloud services where we don't automatically provision accounts and password.
When we manually create such a secret, we store it in 1Password.

This step may have to be done for you by a Phalanx environment administrator depending on how permissions in Vault and any underlying secrets store are handled for your environment.

.. note::

   This document only covers creating a 1Password-backed secret for the first time for an application.
   If you want to update a secret, either by adding new 1Password secrets or by changing their secret values, you should follow the instructions in :doc:`/developers/update-a-onepassword-secret`.

1. Open the 1Password vault
---------------------------

In one password, access the **LSST IT** 1Password team and open the vault for the environment to which you're adding a secret.
If your application will be deployed in multiple environments, you will need to repeat this process for each environment.

The name of the 1Password vault for a given environment is configured in the ``onepassword.vaultTitle`` key in the :file:`values-{environment}.yaml` file in :file:`environments` for that environment.

2. Create the new item
----------------------

Each application should have one entry in the 1Password vault.
Each field in that entry is one Phalanx secret for that application.
The value of the field is the value of the secret.

For a new application, create a new 1Password item of type :guilabel:`Server`.
Delete all of the pre-defined fields.

Then, create a field for each static secret for that application, and set the value to the value of that secret in that environemnt.
The field names should match the secret keys for the application.
Change the field type to password so that the value isn't displayed any time someone opens the 1Password entry.

Do not use sections.
Phalanx requires all of the secret entries be top-level fields outside of any section.

Newlines will be converted to spaces when pasting the secret value.
If newlines need to be preserved, be sure to mark the secret with ``onepassword.encoded`` set to ``true`` in :file:`secrets.yaml`, and then encode the secret in base64 before pasting it into 1Password.

3. Sync 1Password items into Vault
----------------------------------

To sync the new 1Password items into Vault, follow the instructions in :doc:`/admin/sync-secrets`.
This must be done using a Phalanx configuration that includes your new application and the secret configuration for it that you created above.

Next steps
==========

- Add the Argo CD application to appropriate environments: :doc:`add-application`
