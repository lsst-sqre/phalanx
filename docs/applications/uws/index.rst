.. px-app:: uws

#######################################
uws — Universal Worker Service for OCPS
#######################################

The uws application houses services and CSCs associated with the Universal Worker System. The UWS consists of a server that accepts requests to run DM specific jobs, such as calibrations. The application also contains the OCPS CSCs that are associated with each camera. Simulation envrionments do not use simulators for these CSCs.

.. jinja:: uws
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values