.. px-app:: mpc-lookup

#############################################
mpc-lookup — Lookup MPC object by designation
#############################################

This application provides a simple service for looking up Minor Planet Center
(MPC) objects by their designation. Given a valid designation string, the endpoint will automatically redirect to the page for the object on the MPC webpage. The service will also automatically strip out an erroneous prepended string which is present in the DP0.3 designation column.

.. jinja:: mpc-lookup
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values