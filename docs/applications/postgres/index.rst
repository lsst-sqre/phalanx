########
postgres
########

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/postgres <https://github.com/lsst-sqre/phalanx/tree/master/services/postgres>`__
   * - Type
     - Helm_
   * - Namespace
     - ``postgres``

.. rubric:: Overview

The ``postgres`` service is a very small PostgreSQL installation.
It is intended to provide persistent relational storage for low-value databases that it isn't a tragedy to lose.

Do not use this service for important data.
Use a managed relational database such as Google CloudSQL.
Two intended purposes for this service are:

#. The JupyterHub user session database
#. Backing store for Gafaelfawr's authentication tokens

If either of those is destroyed, then all current user sessions and authentication tokens are invalidated, work up to the last checkpoint (5 minutes in JupyterLab) may be lost, and users will have to log in again, restart their sessions, and recreate any authentication tokens.
While irritating, this is not the end of the world; hence "low-value databases."
(That said, production instances of the Science Platform use CloudSQL for the Gafaelfawr token database.)

Upgrading ``postgres`` is generally painless.
A simple Argo CD sync is sufficient.

.. rubric:: Guides

.. toctree::

   recreate-pvc
   add-database
