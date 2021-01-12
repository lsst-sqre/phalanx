###########################
Science Platform operations
###########################

The Science Platform is described in `LDM-542 <https://ldm-542.lsst.io/>`__.
This document contains operational notes of interest to administrators of the Science Platform but not of interest to users.

The Science Platform uses `Argo CD`_ to manage its Kubernetes resources.
The Argo CD configuration and this documentation are maintained on `GitHub <https://github.com/lsst-sqre/lsp-deploy>`__.

Operations guide
================

.. toctree::
   :maxdepth: 2

   argo-cd/index
   cert-issuer/index
   cert-manager/index
   logging/index
   rancher-external-ip-webhook/index
   vault-secrets-operator/index
