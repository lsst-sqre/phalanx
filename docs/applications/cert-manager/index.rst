.. px-app:: cert-manager

######################################
cert-manager — TLS certificate manager
######################################

cert-manager manages TLS certificates internal to the Science Platform Kubernetes cluster.
It may also manage the external TLS certificate for the cluster ingresses if the `Let's Encrypt <https://letsencrypt.org/>`__ approach to certificate management was chosen.

See :ref:`hostnames` for more details on the supported approaches for managing the external TLS certificate.

.. jinja:: cert-manager
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::

   notes
   bootstrap
   route53-setup
   upgrade
   values
