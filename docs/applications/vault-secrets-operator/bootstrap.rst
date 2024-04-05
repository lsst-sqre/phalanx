.. px-app-bootstrap:: vault-secrets-operator

####################################
Bootstrapping vault-secrets-operator
####################################

Vault Secrets Operator is the only component of the Science Platform whose secret has to be manually created, so that it can create the secrets for all other applications.
This will be done automatically by the installer.

AppRole authentication
======================

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

This secret will normally be created by either the installer or by piping :command:`phalanx vault create-read-approle --as-secret vault-credentials` into :command:`kubectl apply`.
This is the default configuration of vault-secrets-operator.

Token authentication
====================

Using a regular Vault token is still supported, but requires special per-environment configuration for vault-secrets-operator.
Put the following into :file:`applications/vault-secrets-operator/values-{environment}.yaml`:

.. code-block:: yaml

   vault-secrets-operator:
     environmentVars:
       - name: "VAULT_TOKEN"
         valueFrom:
           secretKeyRef:
             name: "vault-secrets-operator"
             key: "VAULT_TOKEN"
       - name: "VAULT_TOKEN_LEASE_DURATION"
         value: "31536000"
     vault:
       authMethod: "token"

In this case, the created secret will look like:

.. code-block:: yaml

   apiVersion: v1
   kind: Secret
   metadata:
     name: vault-secrets-operator
     namespace: vault-secrets-operator
   stringData:
     VAULT_TOKEN: <token>
   type: Opaque

This secret will be created by the installer when ``VAULT_TOKEN`` is set in the environment instead of ``VAULT_ROLE_ID`` and ``VAULT_SECRET_ID``.
This Vault token must have raed access (and should not have write access) to the Vault path configured in :file:`environments/values-{environment}.yaml` for your environment.
