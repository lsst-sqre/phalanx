.. px-app:: argocd

#######################################
argocd — Kubernetes application manager
#######################################

`Argo CD`_ is the software that manages all Kubernetes resources in a deployment of the Rubin Science Platform.
It is itself a set of Kubernetes resources and running pods managed with Helm_.

.. jinja:: argocd
   :file: applications/_summary.rst.jinja
   :debug:

Guides
======

.. toctree::

   notes
   bootstrap
   authentication
   upgrade
   values
