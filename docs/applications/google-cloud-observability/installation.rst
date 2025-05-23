.. _installation:

############
Installation
############

#. Enable the Google Cloud `Managed Service for Prometheus`_ via Terraform or the Google Cloud UI.
#. Make sure that the `Managed kube state metrics`_ are NOT enabled.
#. Install the :ref:`grafana app <grafana-app>` in the cluster.
#. Manually `create a Grafana service account`_ and generate a token.
   Unfortunately, the Grafana operator `can't create service accounts`_ yet.
#. Add and sync this token as the ``grafana-datasource-syncer-token`` secret.
#. Manually create a Prometheus datasource in the Grafana UI.
   We can't use a ``GrafanaDatasource`` CRD because we're about to deploy a CronJob who's sole purpose is to modify the datasource every 10 minutes, so it would continually fight with the CRD.
   From the `Google Grafana setup docs`_

   #. Select Add data source, and select Prometheus as the time series database.
   #. Give the data source a name, set the URL field to http://localhost:9090, then select Save & Test. You can ignore any errors saying that the data source is not configured correctly.
   #. Make sure ``Manage alerts via Alerting UI`` is unselected.
#. Note the datasource ID of your new datasource, which will be in the URL if you choose your datasource from the ``connections/datasources`` page.
   It looks lomething like ``bena7r3pg9728f``
#. Add a ``grafana.dtasource.uid`` value in your environment values file with this value.
#. Sync this application
#. Manually create a Job from the ``datasource-syncer`` CronJob (you can do this in ArgoCD) and make sure it succeeds.
#. Go to your datasource in the Grafana UI.
   Make sure the ``Prometheus server URL`` is set to ``https://monitoring.googleapis.com...``, and hit the ``Save & test`` button


.. _Google Grafana setup docs: https://cloud.google.com/stackdriver/docs/managed-prometheus/query#begin
.. _Managed Service for Prometheus: https://cloud.google.com/stackdriver/docs/managed-prometheus
.. _Managed kube state metrics: https://cloud.google.com/kubernetes-engine/docs/how-to/kube-state-metrics#enable-ksm
.. _create a Grafana service account: https://cloud.google.com/stackdriver/docs/managed-prometheus/query#grafana-oauth
.. _can't create service accounts: https://github.com/grafana/grafana-operator/issues/1469

Manual
