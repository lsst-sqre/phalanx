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

The ``postgres`` application is a very small PostgreSQL installation.
It is intended to provide persistent relational storage for low-value
databases that it isn't a tragedy to lose.

Do not use this application for important data.  Use a managed
relational service.  Two applications for this application are:

#. The JupyterHub user session database
#. Backing store for Gafaelfawr's authentication cache.

If either of those is destroyed, then all current user sessions and
authentication are orphaned, work up to the last checkpoint (5 minutes
in JupyterLab) may be lost, and users will have to log in again and
restart their sessions.  While irritating, this is not the end of the
world; hence "low-value databases".

Upgrading ``postgres`` is generally painless.
A simple Argo CD sync is sufficient.

.. rubric:: Guides

.. toctree::

   pvc

