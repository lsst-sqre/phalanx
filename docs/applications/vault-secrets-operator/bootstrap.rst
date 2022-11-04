.. px-app-bootstrap:: vault-secrets-operator

####################################
Bootstrapping vault-secrets-operator
####################################

Vault Secrets Operator is the only component of the Science Platform whose secret has to be manually created, so that it can create the secrets for all other applications.
This will be done automatically by the `install script <https://github.com/lsst-sqre/phalanx/blob/master/installer/install.sh>`__.

Its secret will look like this:

.. code-block:: yaml

   apiVersion: v1
   kind: Secret
   metadata:
     name: vault-secrets-operator
     namespace: vault-secrets-operator
   type: Opaque
   stringData:
     VAULT_TOKEN: <token>
     VAULT_TOKEN_LEASE_DURATION: 86400

Replace ``<token>`` with the ``read`` Vault token for the path ``secret/k8s_operator/<cluster-name>`` in Vault (or whatever Vault enclave you plan to use for this Phalanx environment).
The path must match the path configured in ``values-<environment>.yaml`` in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform>`__.

See :dmtn:`112` for more information.
