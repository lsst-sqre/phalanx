.. px-app:: vault-secrets-operator

.. _vault-secrets-operator:

######################
vault-secrets-operator
######################

The ``vault-secrets-operator`` application is an installation of `Vault Secrets Operator`_ to retrieve necessary secrets from Vault and materialize them as Kubernetes secrets for the use of other applications.
It processes ``VaultSecret`` resources defined in the `phalanx repository`_ and creates corresponding Kubernetes Secret_ resources.

See :dmtn:`112` for the LSST Vault design.

.. jinja:: vault-secrets-operator
   :file: applications/_summary.rst.jinja

.. rubric:: Upgrading

Upgrading to newer upstream releases of the Helm chart is normally simple and straightforward.
We have no significant local customization.

After upgrading, check that Vault Secrets Operator is still working properly by finding a ``VaultSecret`` and ``Secret`` resource pair in the Argo CD dashboard and deleting the ``Secret`` resource.
It should be nearly immediately re-created from the ``VaultSecret`` resource by Vault Secrets Operator.
The Gafaelfawr secret is a good one to use for this purpose since it is only read during Gafaelfawr start-up.

.. rubric:: Bootstrapping

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

Replace ``<token>`` with the ``read`` Vault token for the path ``secret/k8s_operator/<cluster-name>`` in Vault.
See :dmtn:`112` for more information.
