.. px-app:: bigquery-kafka

###################################################
bigquery — BigQuery kafka bridge
###################################################

BigQuery is the backend database used by the Rubin Science Platform for Prompt Processing.
Following from the architecture followed by the QServ-kafka bridge, and in order to make the link between the TAP server and BigQuery less vulnerable to network outages, service restarts, and other transient issues, and to better manage queuing and load, TAP queries are done by putting a request into a Kafka queue and then waiting for the result to be returned in a different Kafka queue.

This service implements the bridge between the Kafka queues and BigQuery.
This application consumes Kafka messages containing job requests, and then uses Google BigQuery's APIs, to run the queries, poll for completion, and upload the resulting VOTable to S3-compatible storage, and sends status messages back to Kafka about the job progress.

For more details on the design, see :sqr:`109` and :sqr:`097`.


.. jinja:: bigquery-kafka
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::

   values
