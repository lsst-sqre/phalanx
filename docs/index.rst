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

Learn about Phalanx's architecture and technologies.

.. toctree::
   :maxdepth: 2

   overview/index

For service developers and maintainers
======================================

Learn how to build services — including websites, web APIs, and other cloud-based infrastructure — and integrate them into Phalanx.

.. toctree::
   :maxdepth: 2

   service-guide/index

For platform administrators
===========================

Learn how to bootstrap and operate a Rubin Science Platform Kubernetes cluster.

.. toctree::
   :maxdepth: 2

   ops/index

Services
========

Learn about the individual services deployed through Phalanx.

.. toctree::
   :maxdepth: 2

   services/index
