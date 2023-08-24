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
Secrets can also be conditional on specific Helm chart settings; in this case, the secret doesn't need to exist unless that Helm setting is true.

For a full specification of the contents of this file, see :doc:`secrets-spec`.

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

Create static secrets in 1Password
==================================

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

Next steps
==========

- Add the Argo CD application to appropriate environments: :doc:`add-application`
