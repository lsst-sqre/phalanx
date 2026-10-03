.. px-app:: river-next

###################################################################
river-next — validation deployment of river with its own ClickHouse
###################################################################

river-next is the validation deployment that replaces :px-app:`river` at
cutover. It runs the same mppdb IVOA TAP front-end as river, but alongside it
the application also runs the ClickHouse server that the front-end queries,
instead of relying on a ClickHouse server outside the Kubernetes cluster.

While it is being validated, river-next is served at ``/river-next`` and its
console is branded ``River @ USDF (next)``, so that it can be compared with
river side by side. At cutover its path becomes ``/river`` (a single value,
``ingress.pathPrefix``), river is retired, and river-next takes over its role.
Until then, river remains the production service.

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
