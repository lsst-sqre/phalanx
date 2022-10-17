.. px-app:: postgres

########
postgres
########

The ``postgres`` service is a very small PostgreSQL installation to provide relational storage for applications and environments where data loss is acceptable.
Two intended purposes for this service are:

- The JupyterHub user session database
- Backing store for Gafaelfawr's authentication tokens

If either of those is destroyed, then all current user sessions and authentication tokens are invalidated, work up to the last checkpoint (five minutes in JupyterLab) may be lost.
Users will have to log in, restart sessions, and recreate authentication tokens.

.. important::

   Do not use this service for important data.
   Use a managed relational database, such as Google CloudSQL, instead.

   Production instances of the Science Platform use CloudSQL for the Gafaelfawr token database instead of this service.

.. jinja:: postgres
   :file: applications/_summary.rst.jinja

Upgrading ``postgres`` is generally painless.
A simple Argo CD sync is sufficient.

Guides
======

.. toctree::
   :maxdepth: 2

   recreate-pvc
   add-database
