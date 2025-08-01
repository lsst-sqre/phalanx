# google-cloud-observability

Google Cloud observability tooling

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| kube-state-metrics | object | See `values.yaml` | Config for kube-state-metrics chart: [values](https://artifacthub.io/packages/helm/prometheus-community/kube-state-metrics/?modal=values) |
| kube-state-metrics.metricAllowlist | list | `["kube_pod_container_status_.*","kube_pod_status_.*","kube_pod_init_container_status_.*","kube_job_status_.*","kube_cronjob_status_.*","kube_persistentvolume_capacity_bytes","kube_persistentvolume_claim_ref","kube_persistentvolume_info","kube_persistentvolume_status_phase","kube_persistentvolumeclaim_info","kube_persistentvolumeclaim_resource_requests_storage_bytes","kube_persistentvolumeclaim_status_phase","kube_deployment_spec_replicas","kube_deployment_status_replicas_available","kube_deployment_status_replicas_updated","kube_statefulset_replicas","kube_statefulset_status_replicas_ready","kube_statefulset_status_replicas_updated","kube_daemonset_status_desired_number_scheduled","kube_daemonset_status_number_misscheduled","kube_daemonset_status_number_ready","kube_daemonset_status_updated_number_scheduled","kube_horizontalpodautoscaler_spec_max_replicas","kube_horizontalpodautoscaler_spec_min_replicas","kube_horizontalpodautoscaler_spec_target_metric","kube_horizontalpodautoscaler_status_condition","kube_horizontalpodautoscaler_status_current_replicas","kube_horizontalpodautoscaler_status_desired_replicas"]` | The specific metrics to collect. This should include at least the [metrics that would be collected from the Google-managed kube-state-metrics](https://cloud.google.com/kubernetes-engine/docs/how-to/kube-state-metrics), since we disable that managed integration. |
| kube-state-metrics.requests | object | `{"cpu":"0.1","memory":"250Mi"}` | See the [resource recommendation docs](https://github.com/kubernetes/kube-state-metrics?tab=readme-ov-file#resource-recommendation) resources: |
