.. _vault-secrets-operator:

######################
vault-secrets-operator
######################

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/vault-secrets-operator <https://github.com/lsst-sqre/phalanx/tree/master/services/vault-secrets-operator>`__
   * - Type
     - Helm_
   * - Namespace
     - ``vault-secrets-operator``

.. rubric:: Overview

The ``vault-secrets-operator`` application is an installation of `Vault Secrets Operator`_ to retrieve necessary secrets from Vault and materialize them as Kubernetes secrets for the use of other applications.
It processes ``VaultSecret`` resources defined in the `Science Platform repository <https://github.com/lsst-sqre/phalanx>`__ and creates corresponding Kubernetes ``Secret`` resources.

.. _Vault Secrets Operator: https://github.com/ricoberger/vault-secrets-operator

See `DMTN-112 <https://dmtn-112.lsst.io>`__ for the LSST Vault design.

.. rubric:: Upgrading

Upgrading to newer upstream releases of the Helm chart is normally simple and straightforward.
We have no significant local customization.

After upgrading, check that Vault Secrets Operator is still working properly by finding a ``VaultSecret`` and ``Secret`` resource pair in the Argo CD dashboard and deleting the ``Secret`` resource.
It should be nearly immediately re-created from the ``VaultSecret`` resource by Vault Secrets Operator.
The Gafaelfawr secret is a good one to use for this purpose since it is only read during Gafaelfawr start-up.

.. rubric:: Bootstrapping the application

Vault Secrets Operator is the only component of the Science Platform whose secret has to be manually created, so that it can create the secrets for all other applications.
This will be done automatically by the `install script <https://github.com/lsst-sqre/phalanx/blob/master/install.sh>`__.

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
See `DMTN-112 <https://dmtn-112.lsst.io>`__ for more information.
