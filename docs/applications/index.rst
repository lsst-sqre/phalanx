############
Applications
############

Applications are individual *atomic* services that are configured and deployed through Phalanx.
Each environment can opt whether to deploy an application, and also customize the configuration of the application.
This section of the documentation describes each Phalanx application.

Applications are divided into several Argo CD projects by type of application.
These groupings are used for access control in some Phalanx environments.
When creating a new Phalanx application, you will choose which of these groupings the application fits best into.

To learn how to develop applications for Phalanx, see the :doc:`/developers/index` section.

.. toctree::
   :maxdepth: 2

   infrastructure
   rsp
   rubin
   roundtable
   monitoring
   prompt
   telescope
