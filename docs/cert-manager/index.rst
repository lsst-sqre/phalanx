############
cert-manager
############

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/cert-manager <https://github.com/lsst-sqre/phalanx/tree/master/services/cert-manager>`__
   * - Type
     - Helm_
   * - Namespace
     - ``cert-manager``

.. rubric:: Overview

The ``cert-manager`` application is an installation of `cert-manager <https://cert-manager.io>`__ from its `Helm chart repository <https://hub.helm.sh/charts/jetstack/cert-manager>`__.
It creates TLS certificates via `Let's Encrypt <https://letsencrypt.org/>`__ and automatically renews them.

See the :doc:`cert-issuer application <../cert-issuer/index>` for how ``cert-manager`` is used.

This application is only deployed on clusters managed by SQuaRE.
NCSA clusters use NCSA certificates issued via an internal process.
IT manages the cert-manager installation on the base and summit Rubin Science Platform clusters.

Upgrading cert-manager is generally painless.
The only custom configuration that we use is to tell the Helm chart to install the Custom Resource Definitions.
Watch for changes that require updating ``ClusterIssuer`` or ``Certificate`` resources; those will require corresponding changes to the resources defined in `/services/cert-issuer <https://github.com/lsst-sqre/phalanx/tree/master/services/cert-issuer>`__.

Normally, it's not necessary to explicitly test cert-manager after a routine upgrade.
We will notice if the certificates expire, and have monitoring of the important ones.
However, if you want to be sure that cert-manager is still working after an upgrade, delete the TLS secret in the ``nublado`` namespace.
It should be recreated by cert-manager.
(You may have to also delete the ``Certificate`` resource of the same name and let Argo CD re-create it to trigger this.)
This may cause an outage for the Science Platform since it is using this certificate, so you may want to be prepared to port-forward to get to the Argo CD UI in case something goes wrong.
