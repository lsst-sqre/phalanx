.. px-app:: river

##############################################################
river — SQL and TAP database of Rubin catalog products at USDF
##############################################################

river is a front-end-only deployment of the mppdb IVOA TAP service, providing
an ADQL/TAP API and a web console over the Rubin catalog products held in an
external ClickHouse server. Note the split: ``river`` is this Kubernetes
application, while ``mppdb`` remains the name of the software it runs, so the
container image, the CLI and every ``MPPDB_*`` setting keep that name.

It answers TAP and ADQL queries by issuing read-only HTTP queries against a
ClickHouse server that is not part of the Kubernetes cluster, so the only state
it holds itself is the SQLite job and state database, the result spool, and the
snapshot manifests, all on a small persistent volume.

Because that state has a single writer, the deployment runs exactly one replica
with the ``Recreate`` update strategy, and its volume is ``ReadWriteOnce``.
Access is authenticated at the ingress by Gafaelfawr, which requires the
``read:tap`` scope, as for every other TAP service in the Science Platform; a
``NetworkPolicy`` makes that ingress the only route to the pod.

Table references must be database-qualified: the service configures no default
database, so ``FROM DiaSource`` is rejected and ``FROM dp2.DiaSource`` is
required. Simple Cone Search resolves against its own configured database,
independently of that, via ``config.scsDatabase``.

This application is USDF-specific: it depends on a ClickHouse server and a
Weka-backed storage class that exist only there.
It should be deployed at ``usdfdev`` first, and elsewhere only after the
back-end catalogs it serves are available in that environment.

.. jinja:: river
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
