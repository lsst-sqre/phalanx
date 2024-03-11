.. px-app:: postgres

###############################
postgres — In-cluster SQL store
###############################

The ``postgres`` service is a very small PostgreSQL installation to provide relational storage for applications and environments where data loss is acceptable.
Two intended purposes for this service are:

- The JupyterHub user session database
- Backing store for Gafaelfawr's authentication tokens

It may also be used by other applications, such as :px-app:`exposurelog` and :px-app:`narrativelog`.

.. important::

   Do not use this service for important data.
   Use a managed relational database, such as Google Cloud SQL, instead.

   Production instances of the Science Platform use Cloud SQL or a local external PostgreSQL server for the Gafaelfawr token database instead of this service.

.. jinja:: postgres
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 2

   add-database
   troubleshoot
   values
