.. px-app:: nublado2

########
nublado2
########

The ``nublado2`` service is an installation of a Rubin Observatory flavor of `Zero to JupyterHub <https://jupyterhub.github.io/helm-chart/>`__ with some additional resources.

.. jinja:: nublado2
   :file: applications/_summary.rst.jinja

Upgrading ``nublado2`` is generally painless.
A simple Argo CD sync is sufficient.

Guides
======

.. toctree::
   :maxdepth: 2

   database
