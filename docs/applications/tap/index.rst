.. px-app:: tap

################################
tap — IVOA Table Access Protocol
################################

TAP (Table Access Protocol) is an IVOA_ service that provides access to general table data, including astronomical catalogs.
On the Rubin Science Platform, it is provided by `lsst-tap-service <https://github.com/lsst-sqre/lsst-tap-service>`__, which is derived from the `CADC TAP service <https://github.com/opencadc/tap>`__.
The data itself, apart from schema queries, comes from Qserv.

.. jinja:: tap
   :file: applications/_summary.rst.jinja


Guides
======

.. toctree::

   notes
   upgrade
   update-tap-schema
   values
