.. px-app:: nublado

############################################
nublado — JupyterHub/JupyterLab for RSP
############################################

The ``nublado`` service is an installation of a Rubin Observatory flavor of `Zero to JupyterHub <https://hub.jupyter.org/helm-chart/>`__ with some additional resources.  This is currently the third version of ``nublado``.
The JupyterHub component provides the Notebook Aspect of the Rubin Science Platform, but replaces the KubeSpawner with a REST client to the JupyterLab Controller.
The JupyterLab Controller component not only provides user lab pod management, but also subsumes the functions formerly provided by the ``cachemachine`` and ``moneypenny`` applications.  That is, in addition to creating and destroying user pods and namespaces, it handles filesystem provisioning for users, and manages prepulls of cached images to local nodes.

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
