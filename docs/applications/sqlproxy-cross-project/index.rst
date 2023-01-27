.. px-app:: sqlproxy-cross-project

#################################################
sqlproxy-cross-project — External Cloud SQL proxy
#################################################

Sometimes, we want to allow arbitrary pods in one Google Kubernetes Engine cluster access Cloud SQL services in a different project.
For example, the IDF dev environment needs to be able to access the Cloud SQL Butler registry in the IDF int environment for testing purposes.

This application enables that type of cross-environment Cloud SQL connection by running a general-use instance of the `Google Cloud SQL Auth Proxy <https://cloud.google.com/sql/docs/postgres/sql-proxy>`__.

.. jinja:: sqlproxy-cross-project
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
