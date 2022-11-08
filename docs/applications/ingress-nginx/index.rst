.. px-app:: ingress-nginx

##################################
ingress-nginx — Ingress controller
##################################

The ``ingress-nginx`` application is an installation of `ingress-nginx <https://kubernetes.github.io/ingress-nginx/>`__ from its `Helm chart <https://github.com/kubernetes/ingress-nginx>`__.
It is used as the ingress controller for all Science Platform applications.

We use ingress-nginx, rather than any native ingress controller, in all Rubin Science Platform environments because we use the NGINX ``auth_request`` feature to do authentication and authorization with :px-app:`gafaelfawr`.
We also apply custom configuration required for correct operation of the Portal Aspect, to support our ``NetworkPolicy`` rules, and to ensure `mostly-correct logging of client IP addresses <https://gafaelfawr.lsst.io/user-guide/prerequisites.html#client-ips>`__.

.. jinja:: ingress-nginx
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 2

   certificates
   values
