############
cert-manager
############

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/cert-manager <https://github.com/lsst-sqre/lsp-deploy/tree/master/services/cert-manager>`__
   * - Type
     - Helm_
   * - Namespace
     - ``cert-manager``

.. rubric:: Overview

The ``cert-manager`` application is an installation of `cert-manager <https://cert-manager.io>`__ from its `Helm chart repository <https://hub.helm.sh/charts/jetstack/cert-manager>`__.
It creates TLS certificates via `Let's Encrypt <https://letsencrypt.org/>`__ and automatically renews them.

This application is only deployed on clusters managed by SQuaRE.
NCSA clusters use NCSA certificates issued via an internal process.

This application is configured to acquire a certificate for the domain name configured via the top-level ``fqdn`` key in the ``values.yaml`` file for a given environment.
This certificate will be stored in the secret ``default-certificate`` in the ``cert-manager`` namespace.
On clusters using cert-manager, nginx-ingress should be configured to use this certificate via this configuration snippet in its ``values.yaml`` file:

.. code-block:: yaml

   nginx-ingress:
     controller:
       extraArgs:
         default-ssl-certificate: cert-manager/default-certificate

.. rubric:: Upgrading

Upgrading cert-manager is generally painless.
The only custom configuration that we use is to tell the Helm chart to install the Custom Resource Definitions.
Watch for changes that require updating ``ClusterIssuer`` or ``Certificate`` resources; those will require corresponding changes to the resources defined in `/services/cert-manager <https://github.com/lsst-sqre/lsp-deploy/tree/master/services/cert-manager>`__.

Normally, it's not necessary to explicitly test cert-manager after a routine upgrade.
We will notice if the certificates expire, and have monitoring of the important ones.
However, if you want to be sure that cert-manager is still working after an upgrade, delete the ``default-certificate`` secret in the ``cert-manager`` namespace.
It should be recreated by cert-manager.
(You may have to also delete the ``Certificate`` resource of the same name and let Argo CD re-create it to trigger this.)
This may cause an outage for nginx-ingress since it is using this certificate, so you may want to be prepared to port-forward to get to the Argo CD UI in case something goes wrong.

.. rubric:: Bootstrapping the application

There are currently two configuration options for cert-manager: the HTTP solver and the DNS solver.
We are standardizing on the DNS solver for all environments for consistency.
The advantage of the DNS solver is that it works behind firewalls and can provision certificates for environments not exposed to the Internet, such as the Tucson teststand.

The DNS solver uses an AWS service user with write access to Route 53 to answer Let's Encrypt challenges.
To configure it, add the following to the ``values.yaml`` file for an environment:

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
