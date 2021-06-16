#######
logging
#######

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/cert-manager <https://github.com/lsst-sqre/phalanx/tree/master/services/logging>`__
   * - Type
     - Helm_
   * - Namespace
     - ``logging``

.. rubric:: Overview

The ``logging`` app deploys Open Distro for Elasticsearch to gather, store, and visualize logs from a Kubernetes cluster.
This is somewhat heavy-weight, so we only run this application on the larger clusters at NCSA, not on the smaller clusters in GKE.

The logging app is built primarily around the ``opendistro-es`` chart maintained in https://github.com/lsst-sqre/charts.
This chart provides Elasticsearch_ and Kibana_ services.
The logging app also includes a ``fluentd-elasticsearch`` chart maintained in https://github.com/kiwigrid/helm-charts.
Fluentd gathers logs from each cluster node and forwards them to Elasticsearch.

.. _Elasticsearch: https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
.. _Kibana: https://www.elastic.co/guide/en/kibana/current/index.html

Kibana is accessible at the ``/logs`` endpoint of the cluster hostname (the same hostname used by Nublado and other Science Platform services).
It will require Gafaelfawr authentication and then password authentication as the shared ``admin`` user.
The ``admin`` password is stored in the SQuaRE 1Password vault under the key "logging passwords."

This chart is a stop-gap so that we have some logging in those clusters.
We have done the bare minimum of configuration required to get Elasticsearch and Kibana up and running.
The application uses a demo configuration, self-signed certificates, and as little tuning as possible.
The hope is that it can be retired in the future in favor of a logging system provided by the Data Facility.
If not, we will need to take the time to properly configure it before it is production-ready.

.. rubric:: Viewing logs

The best place to start exploring log messages is in the Discover tab (the top icon in Kibana below the dim grey line in the left sidebar).

By default you can see every log message from across the entire cluster.
Here are a few tips to help filter the log stream down to just the messages you're interested in:

- **You can filter messages based on the values you see.**
  To do that, mouse over the log messages.
  A magnifying glass appears:

  - **If the message has a value you're interested in,** click the magnifying glass with a "+" symbol inside it.
    Now only messages containing that value are shown.

  - **If the message is one you're not interested in,** click the magnifying glass with a "-" symbol inside it.
    Now messages containing that value aren't shown.

- **Create filters based on Kubernetes labels.**
  For example, a partial pod resource might look like this:

  .. code-block:: yaml

     apiVersion: v1
     kind: Pod
     metadata:
       labels:
         name: myapp

  You can select log messages this pod, and ones like it in a Deployment, based on the ``name: myapp`` label:

  1. Click on the **+ Add filter** button, located below the search bar.

  2. For **field,** enter ``kubernetes.labels.name`` (change as appropriate for the label).

  3. For **operator,** select "``is``."
     Alternatively, "``is in``" is useful for combining multiple log sources together.

  4. For **value,** enter the value of the label (``myapp``, in this example).

- **Create filters based on Kubernetes namespaces** using the field ``kubernetes.namespace_name``, following the same technique as above.

.. rubric:: Upgrading

The underlying components of the logging app (``opendistro-es`` and ``fluentd-elasticsearch``) are monitored by WhiteSource Renovate.
They can be upgraded by merging the normal Renovate PRs.
However, completing the upgrade may require some manual intervention.

The ``fluentd-elasticsearch`` upgrade is normally smooth provided that the Elasticsearch cluster is up.
It deploys agents on every node in the cluster and restarts them one at a time, so it can take some time to complete on a large cluster.

The ``opendistro-es`` upgrade can cause more problems.
Sometimes new versions of the Helm chart will want to make changes to deployments that cannot be patched into the existing deployment.
In this case, you will need to go to the Argo CD console, delete the deployments, and let Argo CD recreate them.

There are four deployments: ``logging-opendistro-es-master``, ``logging-opendistro-es-data``, ``logging-opendistro-es-client``, and ``logging-opendistro-es-kibana``.
The restart is timing-sensitive, since the cluster forms around the nodes seen in a short window of time.
Therefore, if you need to remake the deployments, recreate (via sync) the ``logging-opendistro-es-master`` and ``logging-opendistro-es-data`` services together or in close succession.
Once those services are up and stable, recreate ``logging-opendistro-es-client``, and then finally ``logging-opendistro-es-kibana``.
Be aware that it will take some time for Kibana to start, since it recompiles its JavaScript on each restart.

The health checks for these deployments are sadly worthless.
They will show green even if the service is not healthy.
Checking the logs is more reliable.
The logs for ``logging-opendistro-es-kibana`` in particular will include messges about red or yellow status if the cluster is not working properly.
You can then track down the problem by looking at the logs of the other pods.
``logging-opendistro-es-master`` is normally the most informative.

After an upgrade, the existing data and index configuration may be wiped.
If this happens, you will need to recreate an index.
To do this, go to Kibana (at the ``/logs`` route) and click on the gear icon in the Kibana sidebar and then select **Index Patterns**.
If there are no patterns shown in the resulting screen, select **Create index pattern**.
Use ``*`` as the index pattern and then, on the subsequent screen, use ``@timestamp`` as the timestamp field.
Then, go to **Discover** in the sidebar (the top icon below the thin grey line) and do a search and you should see some data.

.. seealso::

   `The official Kibana Guide <https://www.elastic.co/guide/en/kibana/current/index.html>`__
