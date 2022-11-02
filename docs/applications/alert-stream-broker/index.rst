.. px-app:: alert-stream-broker

###################
Alert Stream Broker
###################

The Alert Stream Broker is responsible for rapid dissemination of alerts (from observatory operations) to community alert brokers.
It is built on top of `Apache Kafka`_ and uses `Apache Avro`_ as the schema for alerts.

For testing during construction, the alert-stream-broker application includes an alert stream simulator, which periodically posts a static set of alerts to allow testing the alert pipeline.
During normal observatory operations, the alerts will instead come from the Alert Production pipelines.

.. jinja:: alert-stream-broker
   :file: applications/_summary.rst.jinja

.. Guides
.. ======
..
.. .. toctree::
..    :maxdepth: 1
