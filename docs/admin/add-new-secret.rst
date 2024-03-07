#######################
Add a new static secret
#######################

Write access to the static secret store is generally limited to environment administrators.
When a developer of an application wants to :doc:`add a new static secret for their application </developers/helm-chart/define-secrets>`, they provide those secrets to the environment administrator, who adds them to the underlying static secret store and ensures Vault is updated.

How to do this depends on where static secrets are stored.

Static secrets in a YAML file
=============================

If the environment stores static secrets in a secure YAML file, the environment administrator should update that file with the newly-required static secrets.
It may be helpful to regenerate the template for that file (see :ref:`admin-secrets-yaml`) and then use :command:`diff` to see what changed.

Then, sync the secrets into Vault following the instructions in :doc:`/admin/sync-secrets`.
This must be done using a Phalanx configuration that includes your new application and the secret configuration for it that you created above.

Static secrets stored directly in Vault
=======================================

If the environment stores static secrets directly in Vault, the environment administrator should add new Vault key/value pairs as needed.
In this case, no sync step is required, since the secrets are used directly from Vault.

In this case, you will need to be sure to store the secrets in the format expected by Phalanx (one secret per application, with keys and values for each Phalanx secret needed by that application).
You will also have to manually set any generated or copied secrets, since you cannot use the normal sync tool.

Static secrets stored in 1Password
==================================

For most SQuaRE-run Phalanx environments, static secrets for applications are stored in a 1Password vault before being automatically synced to the Vault service.
Such secrets are things for external cloud services where we don't automatically provision accounts and password.
When we manually create such a secret, we store it in 1Password.

.. note::

   This document only covers creating a 1Password-backed secret for the first time for an application.
   If you want to update a secret, either by adding new 1Password secrets or by changing their secret values, you should follow the instructions in :doc:`/admin/update-a-secret`.

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
To encode the secret, save it to a file with the correct newlines, and then use a command such as:

.. tab-set::

   .. tab-item:: Linux

      .. prompt:: bash

         base64 -w0 < /path/to/secret; echo ''

   .. tab-item:: macOS

      .. prompt:: bash

         base64 -i /path/to/secret; echo ''

This will generate a base64-encoded version of the secret on one line, suitable for cutting and pasting into the 1Password field.

3. Sync 1Password items into Vault
----------------------------------

To sync the new 1Password items into Vault, follow the instructions in :doc:`/admin/sync-secrets`.
This must be done using a Phalanx configuration that includes your new application and the secret configuration for it that you created above.
