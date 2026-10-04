.. px-app:: river-next

#####################################################
river-next — River with its own ClickHouse server
#####################################################

river-next is the successor to :px-app:`river`. It runs the same mppdb IVOA
TAP front-end as river, but alongside it the application also runs the
ClickHouse server that the front-end queries, instead of relying on a
ClickHouse server outside the Kubernetes cluster.

At ``usdfdev`` it took over river's path, ``/river``, at cutover. The path is a
single value, ``ingress.pathPrefix``, whose chart default ``/river-next`` keeps
it from colliding with river where both are deployed. river stays registered
only for rollback until it is decommissioned.

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
