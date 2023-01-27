.. px-app:: telegraf-ds

###########################################
telegraf-ds — Per-node telemetry collection
###########################################

Telegraf_ is used to gather system metrics about the services running on the Science Platform and send them to a central InfluxDB_ service, where they can be used for dashboards and alerting.

This application deploys a Kubernetes ``DaemonSet`` to gather metrics from every node on the cluster.
For application-level metrics gathering, see the :px-app:`telegraf` application.

.. jinja:: telegraf-ds
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
