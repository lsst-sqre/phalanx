###########################
Science Platform operations
###########################

The Rubin Science Platform is described in `LDM-542 <https://ldm-542.lsst.io/>`__.
This document contains operational notes of interest to administrators of the Science Platform and maintainers of applications deployed via the Science Platform, but not of interest to users.

For user documentation of the Notebook Aspect of the Rubin Science Platform, see `nb.lsst.io <https://nb.lsst.io/>`__.

The Science Platform uses `Argo CD`_ to manage its Kubernetes resources.
The Argo CD configuration and this documentation are maintained on `GitHub <https://github.com/lsst-sqre/phalanx>`__.

A phalanx is a SQuaRE deployment (Science Quality and Reliability Engineering, the team responsible for the Rubin Science Platform).
Phalanx is how we ensure that all of our services work together as a unit.

Overview
========

Intended audience: Anyone who is administering an installation of the Rubin Science Platform or maintaining an application deployed on it.

.. toctree::
   :maxdepth: 2

   introduction
   arch/repository
   arch/secrets

Application maintenance guide
=============================

Intended audience: Maintainers of applications deployed on the Rubin Science Platform.

.. toctree::
   :maxdepth: 2

   app-guide/sync-argo-cd
   app-guide/upgrade
   app-guide/add-application

Operations guide
================

Intended audience: Administrators of an installation of the Rubin Science Platform.

Applications
------------

.. toctree::
   :maxdepth: 2

   ops/argo-cd/index
   ops/cert-issuer/index
   ops/cert-manager/index
   ops/gafaelfawr/index
   ops/ingress-nginx/index
   ops/logging/index
   ops/rancher-external-ip-webhook/index
   ops/squash-api/index
   ops/vault-secrets-operator/index

Bootstrapping
-------------

.. toctree::
   :maxdepth: 2

   ops/bootstrapping
