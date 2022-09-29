#############
ingress-nginx
#############

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/ingress-nginx <https://github.com/lsst-sqre/phalanx/tree/master/services/ingress-nginx>`__
   * - Type
     - Helm_
   * - Namespace
     - ``ingress-nginx``

.. rubric:: Overview

The ``ingress-nginx`` service is an installation of `ingress-nginx <https://kubernetes.github.io/ingress-nginx/>`__ from its `Helm chart <https://github.com/kubernetes/ingress-nginx>`__.
We use NGINX as the ingress controller for all Rubin Science Platform deployments rather than native ingress controllers because we use the NGINX ``auth_request`` feature to do authentication and authorization.

Upgrading ``ingress-nginx`` is generally painless.
A simple Argo CD sync is sufficient.

.. rubric:: Guides

.. toctree::

   certificates
