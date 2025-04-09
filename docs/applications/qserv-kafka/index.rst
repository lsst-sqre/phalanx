.. px-app:: qserv-kafka

################################
qserv-kafka — Qserv Kafka bridge
################################

.. jinja:: qserv-kafka
   :file: applications/_summary.rst.jinja

Qserv is the backend database used by the Rubin Science Platform for visits and related information.
To make the link between the TAP server and Qserv less vulnerable to network outages, service restarts, and other transient issues, and to better manage queuing and load, TAP queries are done by putting a request into a Kafka queue and then waiting for the result to be returned in a different Kafka queue.

This service implements the bridge between the Kafka queues and the Qserv database.
It translates Kafka messages into Qserv's internal APIs, polls Qserv to watch for queries to complete, uploads the resulting VOTable to S3-compatible storage, and sends status messages back to Kafka about the job progress.

For more details on the design, see :sqr:`097`.

Guides
======

.. toctree::
   :maxdepth: 1

   values
