.. px-app:: muster

################################################
muster — Basic testing of Phalanx infrastructure
################################################

Muster is a simple FastAPI application that can be exercised to test basic functionality of a Phalanx environment.
It is used by :px-app:`mobu` to test Gafaelafwr integration with the cluster's ingress controller and other basic support services such as certificate management and Gafaelfawr authentication and authorization.

.. jinja:: muster
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
