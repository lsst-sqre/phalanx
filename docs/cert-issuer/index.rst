###########
cert-issuer
###########

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/cert-issuer <https://github.com/lsst-sqre/lsp-deploy/tree/master/services/cert-issuer>`__
   * - Type
     - Helm_
   * - Namespace
     - ``cert-issuer``

.. rubric:: Overview

The ``cert-issuer`` application creates a cluster issuer for the use of the Rubin Science Platform.
The issuer is named ``cert-issuer-letsencrypt-dns``.
To configure an ingress to use certificates issued by it, add a ``tls`` configuration to the ingress and the annotation:

.. code-block:: yaml

   cert-manager.io/cluster-issuer: cert-issuer-letsencrypt-dns

It depends on `cert-manager <https://cert-manager.io>`__.
On most clusters where the Rubin Science Platform manages certificates, this is also handled by the Rubin Science Platform Argo CD, but on the base and summit clusters, cert-manager is maintained by IT and installed outside of Argo CD.

.. rubric:: Bootstrapping the application

The issuer defined in the ``cert-issuer`` application uses the DNS solver.
The advantage of the DNS solver is that it works behind firewalls and can provision certificates for environments not exposed to the Internet, such as the Tucson teststand.

The DNS solver uses an AWS service user with write access to Route 53 to answer Let's Encrypt challenges.
To configure it, add the following to the ``values-*.yaml`` file for an environment:

.. code-block:: yaml

   solver:
     route53:
       aws-access-key-id: AKIAQSJOS2SFLUEVXZDB
       hosted-zone: Z06873202D7WVTZUFOQ42
       vault-secret-path: "secret/k8s_operator/<cluster-name>/cert-manager"

replacing ``<cluster-name>`` with the FQDN of the cluster, corresponding to the root of the Vault secrets for that cluster.
See :doc:`../vault-secrets-operator/index` for more information.

This access key ID corresponds to the ``cert-manager-lsst-codes`` service user in AWS.
The hosted zone is the ``tls.lsst.codes`` hosted zone, where all challenge responses will be created.
To limit the scope of access in case of a compromise, this AWS service user does not have write access to the full ``lsst.codes`` domain.
This AWS service user can be used for all Science Platform deployments in the ``lsst.codes`` domain.
It is configured according to the `cert-manager documentation for Route 53 <https://cert-manager.io/docs/configuration/acme/dns01/route53/>`__.

The secret key for this AWS access key must be stored in Vault as the ``cert-manager`` secret for that cluster.
The Vault secret should look something like this:

.. code-block:: yaml

   data:
     aws-access-key-id: AKIAQSJOS2SFLUEVXZDB
     aws-secret-access-key: <secret>

The secret is stored in 1Password (search for ``cert-manager-lsst-codes``).
