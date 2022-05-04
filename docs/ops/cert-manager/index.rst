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

The ``cert-manager`` service is an installation of `cert-manager <https://cert-manager.io>`__ from its `Helm chart repository <https://hub.helm.sh/charts/jetstack/cert-manager>`__.
It creates TLS certificates via `Let's Encrypt <https://letsencrypt.org/>`__ and automatically renews them.

This service is only deployed on clusters managed by SQuaRE.
NCSA clusters use NCSA certificates issued via an internal process.

``cert-manager`` creates a cluster issuer that uses the DNS solver and Route 53 for DNS by default.
Set ``config.createIssuer`` to ``false`` for environments where cert-manager should be installed but not use a Route 53 cluster issuer.
For more information, see :ref:`hostnames`.

.. rubric:: Using cert-manager

To configure an ingress to use certificates issued by it, add a ``tls`` configuration to the ingress and the annotation:

.. code-block:: yaml

   cert-manager.io/cluster-issuer: "letsencrypt-dns"

This should be done on one and only one ingress for a deployment using ``cert-manager``.
The RSP conventionally uses the ``squareone`` service.

.. rubric:: Upgrading

Upgrading cert-manager is generally painless.
The only custom configuration that we use, beyond installing a cluster issuer, is to tell the Helm chart to install the Custom Resource Definitions.

Normally, it's not necessary to explicitly test cert-manager after a routine upgrade.
We will notice if the certificates expire, and have monitoring of the important ones.
However, if you want to be sure that cert-manager is still working after an upgrade, delete the TLS secret in the ``squareone`` namespace.
It should be recreated by cert-manager.
(You may have to also delete the ``Certificate`` resource of the same name and let Argo CD re-create it to trigger this.)
This may cause an outage for the Science Platform since it is using this certificate, so you may want to be prepared to port-forward to get to the Argo CD UI in case something goes wrong.

.. rubric:: Guides

.. toctree::

   route53-setup
   bootstrapping

.. seealso::

   * `cert-manager documentation for Route 53 <https://cert-manager.io/docs/configuration/acme/dns01/route53/>`__.
