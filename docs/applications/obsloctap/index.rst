.. px-app:: obsloctap

####################################
obsloctap — Serve observing schedule
####################################

Lookup and reformat ``lsst.sal.Scheduler.logevent_predictedSchedule``.
Return a JSON file of the future observations.
Todo: Also track which observations were made implement ObsLocTAP_ IVOA standard.

.. _ObsLocTAP: https://www.ivoa.net/documents/ObsLocTAP/

.. jinja:: obsloctap
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
