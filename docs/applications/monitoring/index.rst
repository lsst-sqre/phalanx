.. px-app:: monitoring

#########################################
monitoring — Phalanx monitoring framework
#########################################

Monitoring implements an InfluxDBv2 server to collect data from multiple Phalanx deployments.  This server has tasks set up to monitor the health and resource usage of applications within those deployments, and will send alerts to Slack based on those.

Currently it collects the data sent by the :px-app:`telegraf` and :px-app:`telegraf-ds` applications running in individual Phalanx instances.

It also implements a Chronograf UI for analysis of this data.

We expect to migrate the :px-app:`telegraf` and :px-app:`telegraf-ds` applications into it in the near future.

In the slightly longer term, the InfluxDBv2 server will be replaced by InfluxDBv3.

.. jinja:: monitoring
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
