.. px-app:: telegraf

###########################################
telegraf — Application telemetry collection
###########################################

Telegraf_ is used to gather system metrics about the services running on the Science Platform and send them to a central InfluxDB_ service, where they can be used for dashboards and alerting.

This application gathers application-level metrics.
For node-level metrics gathering, see the :px-app:`telegraf-ds` application.

.. jinja:: telegraf
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
