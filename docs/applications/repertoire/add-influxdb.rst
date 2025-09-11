###################################
Add InfluxDB database to Repertoire
###################################

Repertoire supports retrieving connection information for InfluxDB databases, including the username and password that a client should use.
To add a new database, use the following steps.

1. Create a username and password
=================================

Currently, InfluxDB database discovery only supports authentication with username and password.
If the user does not already exist, create a suitable user in InfluxDB with a password.

Normally, this user should be read-only.
Although Repertoire will happily return read/write credentials, this is riskier since they will be accessible to any user with appropriate Gafaelfawr scopes.

2. Store the password in a secret
=================================

Then, add an entry to :file:`applications/repertoire/secrets-{environment}.yaml` for the environment where this InfluxDB connection information will be available.
The entry should look something like this:

.. code-block:: yaml

   idfdev_efd-password:
     description: >-
       InfluxDB password for the efdreader user for accessing the EFD
       database on idfdev. Clients will cache this secret locally in their
       client configuration, so changing it may be disruptive.

The top-level key should be the name of the InfluxDB database label (the label the user will specify when retrieving connection information for that database), followed by ``-password``.

Then, :doc:`update the Repertoire secret </admin/update-a-secret>`.

3. Add the database metadata
============================

Because InfluxDB databases, unlike most other services, may be outside the local Phalanx environment, the list of available databases must be configured for each environment.
This is done in :file:`applications/repertoire/values-{environment}.yaml`.
InfluxDB databases should not be added to :file:`values.yaml`; there are no databases accessible from every environment.

For each database, add a stanza like the following to :file:`values-{environment}.yaml` under ``config.influxdbDatabases``:

.. code-block:: yaml

   idfdev_efd:
     url: "https://data-dev.lsst.cloud/influxdb/"
     database: "efd"
     username: "efdreader"
     passwordKey: "idfdev_efd-password"
     schemaRegistry: "http://sasquatch-schema-registry.sasquatch:8081"

The ``url`` should be the URL to the InfluxDB service.
It does not include the database, but may vary depending on whether clients should use the primary or standby instance, whether InfluxDB Enterprise is in use, and so forth.

The ``database`` is the name of the InfluxDB database to use in queries.
``schemaRegistry`` is the URL to the Confluent Kafka Schema Registry that defines the schema for data in this database.

``username`` and ``passwordKey`` should be set to the username and the secret key set up in step 2.

4. Update the Repertoire application
====================================

Follow the :doc:`normal steps to test Repertoire from a branch </developers/deploy-from-a-branch>`, and then merge the Phalanx PR and sync Repertoire.
The new InfluxDB database information should then be available.

Retrieve the ``/repertoire/discovery`` route to check that the new database appears under ``influxdb_databases``.
If it is correctly listed, there will be a URL under that entry to the connection information.
Retrieve that URL using a web browser or connection authenticated with a token with the ``read:sasquatch`` scope and you should see the JSON version of the information you configured, including the actual password.
