.. px-app-notes:: cert-manager

###################################
Cert-manager architecture and notes
###################################

The :px-app:`cert-manager` service is an installation of `cert-manager <https://cert-manager.io>`__ from its `Helm chart repository <https://artifacthub.io/packages/helm/cert-manager/cert-manager>`__.
It creates cluster-internal private TLS certificates for applications that need them (such as for admission webhooks).
It may also create TLS certificates via `Let's Encrypt <https://letsencrypt.org/>`__ and automatically renew them if the environment uses Let's Encrypt certificates.

``cert-manager`` optionally creates a cluster issuer that uses the DNS solver and Route 53 for DNS.
Set ``config.createIssuer`` to ``false`` for environments where cert-manager should be installed but not use a Route 53 cluster issuer.

For more information on the options for TLS certificate management, see :doc:`/admin/hostnames`.

Using cert-manager
==================

To configure an Ingress_ to use certificates issued by it, add a ``tls`` configuration to the ingress and the annotation:

.. code-block:: yaml

   cert-manager.io/cluster-issuer: "letsencrypt-dns"

Typically, this should be done on one and only one Ingress_ for an environment using ``cert-manager``.
The RSP conventionally uses the :px-app:`squareone` application.
(There are some special exceptions that have their own ingresses or otherwise need valid CA-issued certificates, such as :px-app:`alert-stream-broker` and :px-app:`sasquatch`.)
