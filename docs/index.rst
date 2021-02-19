###########################
Science Platform operations
###########################

The Science Platform is described in `LDM-542 <https://ldm-542.lsst.io/>`__.
This document contains operational notes of interest to administrators of the Science Platform but not of interest to users.

The Science Platform uses `Argo CD`_ to manage its Kubernetes resources.
The Argo CD configuration and this documentation are maintained on `GitHub <https://github.com/lsst-sqre/phalanx>`__.

A phalanx is a SQuaRE deployment (Science Quality and Reliability Engineering, the team responsible for the Rubin Science Platform).
Phalanx is how we ensure that all of our services work together as a unit.

Overview
========

.. toctree::
   :maxdepth: 2

   arch/index
   bootstrapping

Operations guide
================

.. toctree::
   :maxdepth: 2

   argo-cd/index
   cert-issuer/index
   cert-manager/index
   logging/index
   rancher-external-ip-webhook/index
   squash-api/index
   vault-secrets-operator/index
