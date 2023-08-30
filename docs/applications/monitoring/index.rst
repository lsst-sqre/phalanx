.. px-app:: monitoring

#####################################
monitoring — Chronograf monitoring UI
#####################################

Monitoring is an implementation of the Chronograf UI for monitoring the health and resource usage of Phalanx applications.
It runs on the Roundtable environment and provides access to the data sent by the :px-app:`telegraf` and :px-app:`telegraf-ds` applications running in individual RSP instances.

.. jinja:: monitoring
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
