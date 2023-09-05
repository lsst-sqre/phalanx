.. px-app:: rubintv

#####################################
rubintv — Real-time display front end
#####################################

RubinTV is a display front end for various real-time activities on the project.
It is primarily to support and display summit activities, but also serves data from other sites (currently the Tucson Test Stand and the clean room camera testing activities at SLAC).

At the summit, the real-time activities currently include:

.. rst-class:: compact

- AuxTel observing
- ComCam testing
- All sky camera observations
- StarTracker data taking on the TMA
- TMA testing activities

The Rapid Analysis Framework performes realtime analysis on data from these sources, rendering the outputs destined for RubinTV as PNGs, JPEGs, MP4s, and JSON files, which are put in S3 buckets at the summit and at USDF.
The RubinTV frontend then monitors these buckets and serves these files to users.

.. jinja:: rubintv
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
