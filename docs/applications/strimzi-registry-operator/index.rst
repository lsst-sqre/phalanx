.. px-app:: strimzi-registry-operator

############################################################
strimzi-registry-operator — Schema registry for Alert Broker
############################################################

:px-app:`alert-stream-broker` uses `Apache Kafka`_ as the mechanism for publishing alerts.
The `Confluent Schema Registry`_ for that Kafka cluster is created and managed by this installation of the Strimzi Registry Operator.

Note that :px-app:`sasquatch` includes a separate installation of the Strimzi Registry Operator to manage its Confluent Schema Registry.

.. jinja:: strimzi-registry-operator
   :file: applications/_summary.rst.jinja

.. Guides
.. ======
..
.. .. toctree::
..    :maxdepth: 1
