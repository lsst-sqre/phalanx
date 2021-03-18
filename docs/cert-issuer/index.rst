###########
cert-issuer
###########

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/cert-issuer <https://github.com/lsst-sqre/phalanx/tree/master/services/cert-issuer>`__
   * - Type
     - Helm_
   * - Namespace
     - ``cert-issuer``

.. rubric:: Overview

The ``cert-issuer`` application creates a cluster issuer for the use of the Rubin Science Platform.
It depends on `cert-manager <https://cert-manager.io>`__.
The issuer is named ``cert-issuer-letsencrypt-dns``.

On most clusters where the Rubin Science Platform manages certificates, this is also handled by the Rubin Science Platform Argo CD, but on the base and summit clusters, cert-manager is maintained by IT and installed outside of Argo CD.
NCSA clusters use NCSA certificates issued via an internal process.

``cert-issuer`` should only be enabled in environments using Route 53 for DNS and using cert-manager with the DNS solver.
For more information, see :ref:`hostnames`.

.. rubric:: Using cert-issuer

To configure an ingress to use certificates issued by it, add a ``tls`` configuration to the ingress and the annotation:

.. code-block:: yaml

   cert-manager.io/cluster-issuer: cert-issuer-letsencrypt-dns

This should be done on one and only one ingress for a deployment using ``cert-issuer``.
Currently, this is done on the proxy ingress of the ``nublado`` application.
In the future, it will probably move to the ``landing-page`` application.

.. rubric:: Guides

.. toctree::

   route53-setup
   bootstrapping

.. seealso::

   * :doc:`../cert-manager/index`
   * `cert-manager documentation for Route 53 <https://cert-manager.io/docs/configuration/acme/dns01/route53/>`__.
