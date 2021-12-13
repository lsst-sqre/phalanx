###########################################
Add a secret with 1Password and VaultSecret
###########################################

Static secrets for services are stored in a 1Password vault before being automatically synced to the Vault service itself and ultimately to Kubernetes ``Secret`` resources via :ref:`vault-secrets-operator`.
Such secrets are things for external cloud services where we don't automatically provision accounts and password.
When we manually create such a secret, we store it in 1Password.
This page provides steps for adding a service secret through 1Password.

.. note::

   Dynamic secrets that don't have to be coordinated with external resources and only have to be consistent for a given installation of the Science Platform should be generated automatically via the ``SecretGenerator`` class in the `installer/generate_secrets.py <https://github.com/lsst-sqre/phalanx/blob/master/installer/generate_secrets.py>`__ script.
   Those secrets are not stored in 1Password since it's fine for them to change on each installation of the Science Platform.

.. note::

   This document only covers creating a 1Password-backed Secret for the first time for a service.
   If you want to update a Secret, either by adding new 1Password secrets or by changing their secret values, you should follow the instructions in :doc:`/service-guide/update-a-onepassword-secret`.

Part 1. Open the 1Password vault
================================

In one password, access the **LSST IT** 1Password team and open the vault named ``RSP-Vault``.
Items in this vault are synced into Kubernetes ``Secret`` resources.

Part 2. Create a Secret Note
============================

Each item in a Kubernetes ``Secret`` corresponds to either the contents of a secure note or the password field of a login item in 1Password
(Many 1Password items can combined into a single Kubernetes ``Secret`` by configuring the ``VaultSecret``).

- The title of the 1Password item should be formatted as:

  .. code-block:: text

     {{service}} {{env}} {{description}}

  This format is a convention and isn't tied into the automation.
  The ``env`` can be omitted if the secret applies to all environments.

- Add the secret:

  - For a secure note, set the note's **contents** to the secret value.
  - For a login item, set the **password field** to the secret value.

- Add a metadata field labeled ``generate_secrets_key``. The value of that field is formatted as:

  .. code-block:: text

     {{service}} {{secret name}}

  This field provides part of a Vault path for the secret value, which in turn is used by :ref:`vault-secrets-operator` resources to create Kubernetes secrets.

- Add a metadata field labeled ``environment``. The value of that field should be the **hostname** of the RSP environment that this secret applies to (e.g. ``data.lsst.cloud``, not the Phalanx name ``idfprod``).

  If the secret applies to multiple environments, add additional ``environment`` metadata fields for each environment.

  If the secret applies to **all** environments, omit the ``environment`` field altogether.

Part 3. Sync 1Password items into Vault
=======================================

Once a service's secrets are stored in 1Password, you need to sync them into Vault.

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

Next steps: connecting Vault to Kubernetes with VaultSecret
===========================================================

Once a secret is in Vault, you need to create or update a ``VaultSecret`` resource in your services deployment (typically in its Helm_ chart).
See :doc:`create-service` for more details about creating a Helm chart for a service.

A conventional ``VaultSecret`` Helm template looks like this (update ``myapp`` with your service's name):

.. code-block:: yaml

   apiVersion: ricoberger.de/v1alpha1
   kind: VaultSecret
   metadata:
     name: {{ include "myapp.fullname" . }}
     labels:
       {{- include "myapp.labels" . | nindent 4 }}
   spec:
     path: {{ required "vaultSecretsPath must be set" .Values.vaultSecretsPath | quote }}
     type: Opaque

The ``vaultSecretsPath`` Helm variable is configurable through the chart's values (``Values.yaml``).
This Vault path is formatted as:

.. code-block:: text

   secret/k8s_operator/{{host}}/{{service}}

The path components correspond to metadata in 1Password items:

- ``{{host}}`` corresponds to the value of the ``environment`` metadata field
- ``{{service}}`` corresponds to the first part of the ``generate_secrets_key`` metadata field

Within Kubernetes, vault-secrets-operator acts on the ``VaultSecret`` to create a ``Secret`` resource.
The ``Secret`` has the same name and namespace as the ``VaultSecret`` that you explicitly template in your Helm chart.
The generated ``Secret``, though, has secret values that correspond to 1Password items.
The names of the items in the ``Secret`` are the second parts of the ``generate_secrets_key`` metadata field.
