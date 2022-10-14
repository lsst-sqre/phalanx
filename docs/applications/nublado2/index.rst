########
nublado2
########

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/nublado2 <https://github.com/lsst-sqre/phalanx/tree/master/services/nublado2>`__
   * - Type
     - Helm_
   * - Namespace
     - ``nublado2``

.. rubric:: Overview

The ``nublado2`` service is an installation of a Rubin Observatory
flavor of Zero to JupyterHub with some additional resources.  Those
resources are defined from `templates at <https://github.com/lsst-sqre/phalanx/tree/master/services/nublado2/templates>`__ and the `Zero to Jupyterhub chart <https://jupyterhub.github.io/helm-chart/>`__.

Upgrading ``nublado2`` is generally painless.
A simple Argo CD sync is sufficient.

.. rubric:: Guides

.. toctree::

   database
