.. px-app:: ingress-nginx

#############
ingress-nginx
#############

The ``ingress-nginx`` application is an installation of `ingress-nginx <https://kubernetes.github.io/ingress-nginx/>`__ from its `Helm chart <https://github.com/kubernetes/ingress-nginx>`__.
We use NGINX as the ingress controller for all Rubin Science Platform deployments rather than native ingress controllers because we use the NGINX ``auth_request`` feature to do authentication and authorization.

.. jinja:: ingress-nginx
   :file: applications/_summary.rst.jinja

.. rubric:: Overview

Upgrading ``ingress-nginx`` is generally painless.
A simple Argo CD sync is sufficient.

Guides
======

.. toctree::
   :maxdepth: 2

   certificates
