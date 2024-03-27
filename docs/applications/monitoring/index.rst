.. px-app:: monitoring

#########################################
monitoring — Phalanx monitoring framework
#########################################

Monitoring implements several components.  The ``telegraf`` component is expected to run almost everywhere (and therefore the app will be enabled almost everywhere), and will send its data to a central InfluxDBv2 server.

There is a separate application :px-app:`telegraf-ds`, which must remain separate for now, because ``telegraf`` and ``telegraf-ds`` cannot be subcharts of the same chart due to a bug in their helm charts.
:px-app:`telegraf-ds` is also expected to run almost everywhere.

The other components of ``monitoring`` should be global singletons (or if not global, at least, "only one per administrative grouping of Phalanx environments").
That is to say: only a single collection point is needed to monitor an arbitrary collection of Phalanx environments.

The ``monitoring`` application implements an InfluxDBv2 server to collect data from multiple Phalanx deployments.
This server has tasks set up to monitor the health and resource usage of applications within those deployments, and will send alerts to Slack based on those.

It also implements a Chronograf UI for analysis of this data.

In the slightly longer term, the InfluxDBv2 server will be replaced by InfluxDBv3.

Installation
============

If you are not running the collection server (that is, the influxdb2 component, and likely the cronjobs and the Chronograf UI), all you need to do is enable the telegraf component.

Secret creation still requires definition of many fields, but everything except ``telegraf-token`` and ``influx-org`` can be set to a dummy value, since the agents only need to know how to send data to the central InfluxDBv2 server.

However, if you are running the server-side pieces of ``monitoring``, it is complex and has many points of contact with both other Phalanx components, notably Gafaelfawr, and external systems, such as Slack.  There are, unfortunately, a lot of manual steps in the installation.

There are both ``preinstall`` and ``postinstall`` instructions
for ``monitoring`` installation.  Doing them in order is highly
recommended.


.. jinja:: monitoring
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 2

   preinstall
   install
   postinstall
   values
