.. px-app:: auxtel

######################################################
auxtel — Auxiliary Telescope Control System Components
######################################################

The auxtel application houses the CSCs associated with the Auxiliary Telescope. Simulation environments use simulators for all CSCs except the ATAOS, ATDomeTrajectory, ATHeaderService, ATOODS and ATPtg. Those environments also contain a simulator for the low-level controller of the ATHexapod.

.. jinja:: auxtel
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values