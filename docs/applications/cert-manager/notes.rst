.. px-app-notes:: cert-manager

###################################
Cert-manager architecture and notes
###################################

The :px-app:`cert-manager` service is an installation of `cert-manager <https://cert-manager.io>`__ from its `Helm chart repository <https://artifacthub.io/packages/helm/cert-manager/cert-manager>`__.
It creates TLS certificates via `Let's Encrypt <https://letsencrypt.org/>`__ and automatically renews them.

This application is only deployed on clusters managed by SQuaRE on Google Cloud Platform.
If a site uses some other process to manage its certificates, it is the responsibility of that site's administrative team to acquire and deploy those certificates.

``cert-manager`` creates a cluster issuer that uses the DNS solver and Route 53 for DNS by default.
Set ``config.createIssuer`` to ``false`` for environments where cert-manager should be installed but not use a Route 53 cluster issuer.
For more information, see :ref:`hostnames`.

.. seealso::

   `cert-manager documentation for Route 53 <https://cert-manager.io/docs/configuration/acme/dns01/route53/>`__.

Using cert-manager
==================

To configure an Ingress_ to use certificates issued by it, add a ``tls`` configuration to the ingress and the annotation:

.. code-block:: yaml

   cert-manager.io/cluster-issuer: "letsencrypt-dns"

This should be done on one and only one Ingress_ for an environment using ``cert-manager``.
The RSP conventionally uses the :px-app:`squareone` application.
