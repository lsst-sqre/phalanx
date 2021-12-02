###########################
Science Platform operations
###########################

The Rubin Science Platform is described in `LDM-542 <https://ldm-542.lsst.io/>`__.
This document contains operational notes of interest to administrators of the Science Platform and maintainers of services deployed via the Science Platform, but not of interest to users.

For user documentation of the Notebook Aspect of the Rubin Science Platform, see `nb.lsst.io <https://nb.lsst.io/>`__.

The Science Platform uses `Argo CD`_ to manage its Kubernetes resources.
The Argo CD configuration and this documentation are maintained on `GitHub <https://github.com/lsst-sqre/phalanx>`__.

A phalanx is a SQuaRE deployment (Science Quality and Reliability Engineering, the team responsible for the Rubin Science Platform).
Phalanx is how we ensure that all of our services work together as a unit.

Overview
========

.. toctree::
   :maxdepth: 2

   introduction
   arch/repository
   arch/secrets

For service maintainers
=======================

General development and operations
----------------------------------

.. toctree::
   :maxdepth: 2

   service-guide/create-service
   service-guide/add-a-onepassword-secret
   service-guide/add-service
   service-guide/add-external-chart
   service-guide/sync-argo-cd
   service-guide/upgrade
   service-guide/chart-changes

Specific tasks
--------------

.. toctree::
   :maxdepth: 2

   service-guide/update-tap-schema
   service-guide/mobu-manage-flocks

For science platform administrators
===================================

Services
--------

.. toctree::
   :maxdepth: 2

   ops/argo-cd/index
   ops/cachemachine/index
   ops/cert-issuer/index
   ops/cert-manager/index
   ops/gafaelfawr/index
   ops/ingress-nginx/index
   ops/nublado2/index
   ops/postgres/index
   ops/rancher-external-ip-webhook/index
   ops/squash-api/index
   ops/tap/index
   ops/vault-secrets-operator/index

Bootstrapping
-------------

.. toctree::
   :maxdepth: 3

   ops/bootstrapping

Infrastructure
--------------

.. toctree::
  :maxdepth: 2

  ops/infrastructure/filestore/index

Troubleshooting
---------------

.. toctree::
   :maxdepth: 2

   ops/troubleshooting
