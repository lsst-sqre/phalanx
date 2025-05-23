.. px-app:: google-cloud-observability

###############################################################
google-cloud-observability — Google Cloud observability tooling
###############################################################

.. jinja:: google-cloud-observability
   :file: applications/_summary.rst.jinja

Google provides a `managed service for Prometheus`_.
In Phalanx environments provisioned on `GKE`_, we'd like to use this for as much as we can to avoid the effort of running our own metrics and monitoring infrastructure.
Unfortunately, the `managed kube-state-metrics`_ package does not provide ``kube_pod_container_status_last_terminated_reason`` or ``kube_pod_container_status_restarts_total``, both of which are needed to alert on container OOM kills in the most reliable way.
This app installs our own `kube-state-metrics`_ and configures the Google Cloud managed service for Prometheus to scrape it.

.. _managed service for Prometheus: https://cloud.google.com/stackdriver/docs/managed-prometheus
.. _GKE: https://cloud.google.com/kubernetes-engine
.. _managed kube-state-metrics: https://cloud.google.com/kubernetes-engine/docs/how-to/kube-state-metrics
.. _kube-state-metrics: https://github.com/kubernetes/kube-state-metrics

Prerequisites
=============

* Managed service for Prometheus is installed in the GKE cluster.
  This is probably configured in the `idf_deploy repo`_.

.. _idf_deploy repo: https://github.com/lsst/idf_deploy

Guides
======

.. toctree::
   :maxdepth: 1

   values
