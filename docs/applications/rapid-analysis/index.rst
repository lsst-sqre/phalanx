.. px-app:: rapid-analysis

#################################################
rapid-analysis — Real-time backend of the RubinTV
#################################################

The Rapid Analysis Framework performes realtime analysis on data from these sources, rendering the outputs destined for RubinTV as PNGs, JPEGs, MP4s, and JSON files, which are put in S3 buckets at the summit and at USDF.
The RubinTV frontend then monitors these buckets and serves these files to users.

At the summit, the real-time activities currently include:

.. rst-class:: compact

- AuxTel observing
- ComCam testing
- All sky camera observations
- StarTracker data taking on the TMA
- TMA testing activities

.. jinja:: rapid-analysis
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
