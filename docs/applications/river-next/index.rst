.. px-app:: river-next

#####################################################
river-next — River with its own ClickHouse server
#####################################################

river-next serves River, an mppdb IVOA TAP service for Rubin catalogs, at
``/river``. It replaced the earlier ``river`` application, which used a
ClickHouse server outside the Kubernetes cluster. river-next brings its own
ClickHouse server: as a StatefulSet in the cluster, or on an external host
reached through the native Weka client.

``clickhouse.backend`` selects which. With ``pod``, the StatefulSet runs the
server, and the front-end queries it through the in-cluster Service. With
``external``, the StatefulSet is scaled to zero, and the front-end queries
``clickhouse.external.host`` instead. That host runs the same server image and
configuration on the same data directory. A guard (an init container, plus a
wrapper around the server process) makes sure only one side ever runs on that
directory. At ``usdfdev`` the server runs on the external host.

The URL path is a single value, ``ingress.pathPrefix``, whose chart default is
``/river-next``.

The front-end keeps its own state: the SQLite job and state database and the
snapshot manifests on one persistent volume, and the async result spool on
another. Because that state has a single writer, the front-end runs exactly one
replica with the ``Recreate`` update strategy, on ``ReadWriteOnce`` volumes.
Access is authenticated at the ingress by Gafaelfawr, which requires the
``read:tap`` scope, as for every other TAP service in the Science Platform.

Table references must be database-qualified: the service configures no default
database, so ``FROM DiaSource`` is rejected and ``FROM dp2.DiaSource`` is
required. Simple Cone Search resolves against its own configured database,
independently of that, via ``config.scsDatabase``.

This application is USDF-specific: it depends on USDF storage classes and on
data that exist only there, and it is deployed only at ``usdfdev``.

.. jinja:: river-next
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
