.. px-app:: repertoire

##############################
repertoire — Service discovery
##############################

.. jinja:: repertoire
   :file: applications/_summary.rst.jinja

Repertoire_ is the data and service discovery mechanism for Phalanx.
It provides an API for services to discover information about the local environment, most notably but not limited to the base URLs of other services.
It also provides connection information and credentials for InfluxDB databases managed by Sasquatch in either the local environment or an accessible remote environment.

See :dmtn:`250` for the specification for Phalanx service discovery, which Repertoire partially implements.

Guides
======

.. toctree::
   :maxdepth: 1

   add-service
   add-influxdb
   values
