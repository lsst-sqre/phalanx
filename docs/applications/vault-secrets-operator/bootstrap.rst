.. px-app-bootstrap:: vault-secrets-operator

####################################
Bootstrapping vault-secrets-operator
####################################

Vault Secrets Operator is the only component of the Science Platform whose secret has to be manually created, so that it can create the secrets for all other applications.
This will be done automatically by the `install script <https://github.com/lsst-sqre/phalanx/blob/main/installer/install.sh>`__.

When using the newer, recommended :ref:`secrets management system <admin-vault-credentials>`, the secret created by the installer will look like this:

.. code-block:: yaml

   apiVersion: v1
   kind: Secret
   metadata:
     name: vault-credentials
     namespace: vault-secrets-operator
   stringData:
     VAULT_ROLE_ID: <role-id>
     VAULT_SECRET_ID: <secret-id>
   type: Opaque

This secret will normally be created by either the installer or :command:`phalanx vault create-read-approle`.

Using a regular Vault token is still supported, in which case the secret will look like this:

.. code-block:: yaml

   apiVersion: v1
   kind: Secret
   metadata:
     name: vault-secrets-operator
     namespace: vault-secrets-operator
   stringData:
     VAULT_TOKEN: <token>
   type: Opaque

This secret will be created by the installer when given a ``VAULT_TOKEN`` parameter.

In either case, the Vault token or AppRole must have read access to the Vault path configured in :file:`environments/values-{environment}.yaml` for your environment.
