############
cachemachine
############

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/cachemachine <https://github.com/lsst-sqre/phalanx/tree/master/services/cachemachine>`__
   * - Type
     - Helm_
   * - Namespace
     - ``cachemachine``

.. rubric:: Overview

The ``cachemachine`` application is an installation of the RSP's
image-prepulling service from its `Helm chart <https://github.com/lsst-sqre/charts/tree/master/charts/cachemachine>`__.

Upgrading ``cachemachine`` is generally painless.
A simple Argo CD sync is sufficient.

.. rubric:: Guides

.. toctree::

   pruning
   updating_recommended
