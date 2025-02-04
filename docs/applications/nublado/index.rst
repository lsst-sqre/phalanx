.. px-app:: nublado

#######################################
nublado — JupyterHub/JupyterLab for RSP
#######################################

The Nublado application provides a JupyterHub and JupyterLab interface for Rubin Science Platform users.
It includes a Kubernetes controller that, besides creating user lab pods, prepulls lab images and can provide per-user WebDAV file servers.

The JupyterHub component and its proxy are deployed via `Zero to JupyterHub <https://hub.jupyter.org/helm-chart/>`__ with a custom configuration.
The Nublado controller is deployed alongside it as a separate FastAPI service.

Nublado user pods are created under the ``nublado-users`` Argo CD application.
WebDAV file servers are created in the ``fileservers`` Kubernetes namespace and the ``nublado-fileservers`` Argo CD application.

.. jinja:: nublado
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 2

   bootstrap
   upgrade
   major-upgrade
   clean-up-labs
   block-spawns
   updating-recommended
   troubleshoot
   values
