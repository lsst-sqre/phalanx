.. px-app:: obstap

###########################################
obstap — IVOA OBSCore Table Access Protocol
###########################################

OBSTAP_ (OBSCore Table Access Protocol) is an IVOA_ service that provides access to the ObsCore table which is hosted on postgres.
On the Rubin Science Platform, it is provided by `tap-postgres <https://github.com/lsst-sqre/tap-postgres>`__, which is derived from the `CADC TAP service <https://github.com/opencadc/tap>`__.
This service provides access to the ObsTAP tables that are created and served by the butler.

The TAP data itself, apart from schema queries, comes from Postgres.
The TAP schema is provided by the separate :px-app:`tap-schema` application.

See :px-app-upgrade:`tap-schema` for information on how to update the TAP schema.

.. jinja:: tap
   :file: applications/_summary.rst.jinja


Guides
======

.. toctree::

   notes
   values
