.. px-app:: nublado

#######################################
nublado — JupyterHub/JupyterLab for RSP
#######################################

The ``nublado`` application provides a JupyterHub and JupyterLab interface for Rubin Science Platform users.
It also deploys a Kubernetes controller that, besides creating user lab pods, prepulls lab images and can provide per-user WebDAV file servers.

The JupyterHub component and its proxy is deployed via `Zero to JupyterHub <https://hub.jupyter.org/helm-chart/>`__ with a custom configuration.
Alongside it, the Nublado controller is deployed by the same application as a separate FastAPI service.

.. jinja:: nublado
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 2

   bootstrap
   upgrade
   major-upgrade
   updating-recommended
   troubleshoot
   values
