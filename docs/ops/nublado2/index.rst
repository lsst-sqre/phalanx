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

The ``nublado2`` service is an installation of JupyterHub from its `Helm chart <https://github.com/lsst-sqre/charts/tree/master/charts/nublado2>`__.

Upgrading ``nublado2`` is generally painless.
A simple Argo CD sync is sufficient.

.. rubric:: Guides

.. toctree::

   database
