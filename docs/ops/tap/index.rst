###
TAP
###

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/tap <https://github.com/lsst-sqre/phalanx/tree/master/services/tap>`__
   * - Type
     - Helm_
   * - Namespace
     - ``tap``

.. rubric:: Overview

TAP (Table Access Protocol) is an IVOA_ service that provides access to general table data, including astronomical catalogs.
On the Rubin Science Platform, it is provided by `lsst-tap-service <https://github.com/lsst-sqre/lsst-tap-service>`__, which is derived from the `CADC TAP service <https://github.com/opencadc/tap>`__.
The data itself, apart from schema queries, comes from qserv.

The ``tap`` service consists of the TAP Java web service, a PostgreSQL database used to track user job submissions, and (on development deployments) a mock version of qserv.

Upgrading ``tap`` normally only requires an Argo CD sync.

.. rubric:: Architecture

.. figure:: /_static/notebook-tap.png
   :name: Flow for Notebook Aspect queries to TAP

   Flow for Notebook Aspect queries to TAP

.. figure:: /_static/portal-tap.png
   :name: Flow for Portal Aspect queries to TAP

   Flow for Portal Aspect queries to TAP
