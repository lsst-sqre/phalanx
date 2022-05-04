##########
squash-api
##########

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/squash-api <https://github.com/lsst-sqre/phalanx/tree/master/services/squash-api>`__
   * - Type
     - Helm_
   * - Namespace
     - ``squash-api``

.. rubric:: Overview

The ``squash-api`` app deploys a REST API for managing Science Pipelines metrics.
You can learn more about SQuaSH in SQR-009_.

.. _SQR-009: https://sqr-009.lsst.io/

Currently, the ``squash-api`` is deployed using the ``squash-sandbox`` and ``squash-prod`` environments along with other services:

- argo-cd
- cert-manager
- chronograf
- gafaelfawr
- influxdb
- kapacitor
- ingress-nginx
- vault-secrets-operator

You can reach the following services, for example, for the ``https://squash-sandbox.lsst.codes`` deployment:

- https://squash-sandbox.lsst.codes (SQuaSH API)
- https://squash-sandbox.lsst.codes/argo-cd  (Argo CD)
- https://squash-sandbox.lsst.codes/chronograf (Chronograf)
- https://squash-sandbox.lsst.codes/influxdb (InfluxDB)

The Science Pipelines use lsst.verify_ to collect metrics and their measurements and produce verification jobs that are uploaded to the SQuaSH API.
An internal task in the SQuaSH API extracts metric values and metadata from the verification jobs and stores them in InfluxDB.

.. _lsst.verify: https://sqr-019.lsst.io/

Chronograf is the UI for displaying measurements of the Science Pipeline metrics and it uses Gafaelfawr to authenticate users with the CILogon provider.

.. rubric:: SQuaSH data migration

Here we document the steps to migrate data from an existing SQuaSH instance to a new one.
To exemplify this, let's assume we want to migrate data from https://squash-prod.lsst.codes to https://squash-sandbox.lsst.codes to make a clone of the production instance.

The SQuaSH API uses a MySQL instance, managed by CloudSQL, to store the Science Pipelines verification jobs.
The steps to clone the CloudSQL instance are:

* Clone the ``squash-db-prod`` database in CloudSQL to a new instance, e.g. ``squash-db-sandbox-N``, where N is an incremental number.
* Update the database user credentials, they have to match the the ``squash-db-user`` and ``squash-db-password`` keys in the ``squash-api`` secret for the new https://squash-sandbox.lsst.codes deployment.
* Update ``instanceConnectionName:`` in ``services/squash-api/values-squash-sandbox.yaml`` to the new value.
* Synchronize the ``squash-api`` app in https://squash-sandbox.lsst.codes/argo-cd to connect to the Cloud SQL instance clone.

You can check if the connection was successful by inspecting the logs of the ``cloudsql-proxy`` container in the ``squash-api`` pod.

To migrate InfluxDB databases use the ``dump.sh`` and ``restore.sh`` scripts in  `squash-api/scripts/ <https://github.com/lsst-sqre/squash-api/tree/master/scripts>`_.

First, set the ``kubectl`` context of the source InfluxDB instance (https://squash-prod.lsst.codes) then run:

.. code::

  ./dump.sh influxdb squash-prod  # this database stores measurements of the science pipelines metrics
  ./dump.sh influxdb chronograf # this database stores chronograf data such as annotations and the alert history

where ``influxdb`` is the namespace of the InfluxDB deployment, and the second argument is the name of the database to dump.

Before running the ``restore.sh`` script, set the ``kubectl`` context of the destination InfluxDB instance (https://squash-sandbox.lsst.codes).
Then use the output directory from the ``dump.sh`` command as the input directory for the ``restore.sh`` command:

.. code::

  ./restore.sh influxdb squash-prod <input-dir>
  ./restore.sh influxdb chronograf <input-dir>

where ``influxdb`` is the namespace of the InfluxDB deployment, and the second argument is the name of the database to restore.

In addition to the MySQL CloudSQL instance and the InfluxDB databases, there are two other context databases that need to be restored.
The Chronograf context database stores users, organizations, connection data to InfluxDB and Kapacitor, and dashboard data.
The Kapacitor database stores the alert rules and TICKScritps.

To restore the Chronograf and Kapacitor databases set the ``kubectl`` context of the source instance and copy the files:

.. code::

  kubectl cp chronograf/<chronograf-pod>:var/lib/chronograf/chronograf-v1.db chronograf-v1.db
  kubectl cp kapacitor/<kapacitor-pod>:var/lib/kapacitor/kapacitor.db kapacitor.db

Set the ``kubectl`` context of the destionation instance, copy the database files to the same location into the corresponding pods, and then restart the pods for that to take effect.
