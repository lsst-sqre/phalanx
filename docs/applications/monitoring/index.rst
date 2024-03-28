.. px-app:: monitoring

######################################
monitoring — Phalanx monitoring server
######################################

Only a single collection point is needed to monitor an arbitrary collection of Phalanx environments, so you will only have one instance of ``monitoring`` for all the Phalanx environments in a particular administrative grouping (more or less: managed by the same team, but this is a social rather than a technical grouping).

The ``monitoring`` application implements an InfluxDBv2 server to collect data from multiple Phalanx deployments.

This server has periodic tasks set up to monitor the health and resource usage of applications within those deployments, and will send alerts to Slack based on those.

It also implements a Chronograf UI for analysis of this data.

The InfluxDBv2 server will be replaced by InfluxDBv3 at some point in the hopefully-fairly-near future.


Installation
============

The ``monitoring`` application is complex and has many points of contact with both other Phalanx components, notably Gafaelfawr, and external systems, such as Slack.  There are, unfortunately, a lot of manual steps in the installation.

There are both ``preinstall`` and ``postinstall`` instructions for ``monitoring`` installation.  Doing them in order is highly recommended.


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
