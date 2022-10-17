.. px-app:: tap

###
tap
###

TAP (Table Access Protocol) is an IVOA_ service that provides access to general table data, including astronomical catalogs.
On the Rubin Science Platform, it is provided by `lsst-tap-service <https://github.com/lsst-sqre/lsst-tap-service>`__, which is derived from the `CADC TAP service <https://github.com/opencadc/tap>`__.
The data itself, apart from schema queries, comes from Qserv.

.. jinja:: tap
   :file: applications/_summary.rst.jinja

.. rubric:: Architecture

The ``tap`` application consists of the TAP Java web application, a PostgreSQL database used to track user job submissions, and (on development deployments) a mock version of qserv.

.. diagrams:: notebook-tap.py

.. diagrams:: portal-tap.py

Upgrading ``tap`` normally only requires an Argo CD sync.

Guides
======

.. toctree::

   update-tap-schema
