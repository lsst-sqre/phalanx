.. px-app:: tap

################################
tap — IVOA Table Access Protocol
################################

TAP_ (Table Access Protocol) is an IVOA_ service that provides access to general table data, including astronomical catalogs.
On the Rubin Science Platform, it is provided by https://github.com/lsst-sqre/lsst-tap-service, which is derived from the `CADC TAP service <https://github.com/opencadc/tap>`__.
The same service provides both TAP and ObsTAP_ schemas.

The TAP data itself, apart from schema queries, comes from Qserv.
The TAP schema is provided by images built from https://github.com/lsst/sdm_schemas.

.. jinja:: tap
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::

   notes
   values
