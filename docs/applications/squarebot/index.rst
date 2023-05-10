.. px-app:: squarebot

###############################
squarebot — Kafka event gateway
###############################

Squarebot feeds events from services like Slack and GitHub into the SQuaRE Events Kafka message bus running on Roundtable. Backend apps like Templatebot can subscribe to these events and take domain-specific action.

.. jinja:: squarebot
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
