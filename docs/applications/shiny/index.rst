.. px-app:: shiny

##################################################
shiny — TAP query front end for the mppdb catalogs
##################################################

shiny is a front-end-only deployment of the mppdb IVOA TAP service.
It answers TAP and ADQL queries by issuing read-only HTTP queries against an
external ClickHouse server that is not part of the Kubernetes cluster, so the
only state it holds itself is the SQLite job and state database, the result
spool, and the snapshot manifests, all on a small persistent volume.

Because that state has a single writer, the deployment runs exactly one replica
with the ``Recreate`` update strategy, and its volume is ``ReadWriteOnce``.
Access is authenticated at the ingress by Gafaelfawr, which requires the
``read:tap`` scope, as for every other TAP service in the Science Platform; a
``NetworkPolicy`` makes that ingress the only route to the pod.

This application is USDF-specific: it depends on a ClickHouse server and a
Weka-backed storage class that exist only there.
It should be deployed at ``usdfdev`` first, and elsewhere only after the
back-end catalogs it serves are available in that environment.

.. jinja:: shiny
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
