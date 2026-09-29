.. px-app:: repertoire

##############################
repertoire — Service discovery
##############################

.. jinja:: repertoire
   :file: applications/_summary.rst.jinja

Repertoire_ is the data and service discovery mechanism for Phalanx.
It provides an API for services to discover information about the local environment, most notably but not limited to the base URLs of other services.
It provides connection information and credentials for InfluxDB databases managed by Sasquatch in either the local environment or an accessible remote environment.
Repertoire also manages ``TAP_SCHEMA`` metadata for TAP services using Cloud SQL or an external PostgreSQL databases.

See the `Repertoire operational documentation <https://repertoire.lsst.io/operations/>`__ for information about how to add a new service or dataset, or how to configure ``TAP_SCHEMA`` schema versions and available schemas per TAP service.

See :dmtn:`250` for the specification for Phalanx service discovery, which Repertoire partially implements.

Guides
======

.. toctree::
   :maxdepth: 1

   add-influxdb
   values
