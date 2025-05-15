# victoria-metrics

Operational metrics database

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| externalGrafanaOperator.installed | bool | `true` |  |
| externalGrafanaOperator.pathPrefix | string | `"grafana"` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| vmstack.alertmanager.config.inhibit_rules[0].equal[0] | string | `"cluster"` |  |
| vmstack.alertmanager.config.inhibit_rules[0].equal[1] | string | `"namespace"` |  |
| vmstack.alertmanager.config.inhibit_rules[0].source_matchers[0] | string | `"alertname=InfoInhibitor"` |  |
| vmstack.alertmanager.config.inhibit_rules[0].target_matchers[0] | string | `"severity=info"` |  |
| vmstack.alertmanager.config.receivers[0].name | string | `"blackhole"` |  |
| vmstack.alertmanager.config.receivers[1].name | string | `"slack-monitoring"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[0].text | string | `"Runbook :green_book:"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[0].type | string | `"button"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[0].url | string | `"{{ (index .Alerts 0).Annotations.runbook_url }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[1].text | string | `"Query :mag:"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[1].type | string | `"button"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[1].url | string | `"{{ (index .Alerts 0).GeneratorURL }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[2].text | string | `"Dashboard :grafana:"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[2].type | string | `"button"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[2].url | string | `"{{ (index .Alerts 0).Annotations.dashboard }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[3].text | string | `"Silence :no_bell:"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[3].type | string | `"button"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[3].url | string | `"{{ template \"__alert_silence_link\" . }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[4].text | string | `"{{ template \"slack.monzo.link_button_text\" . }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[4].type | string | `"button"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].actions[4].url | string | `"{{ .CommonAnnotations.link_url }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].api_url_file | string | `"/etc/alertmanager/slack-config/slack-alert-webhook"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].color | string | `"{{ template \"slack.monzo.color\" . }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].icon_emoji | string | `"{{ template \"slack.monzo.icon_emoji\" . }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].send_resolved | bool | `true` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].text | string | `"{{ template \"slack.monzo.text\" . }}"` |  |
| vmstack.alertmanager.config.receivers[1].slack_configs[0].title | string | `"{{ template \"slack.monzo.title\" . }}"` |  |
| vmstack.alertmanager.config.route.group_by[0] | string | `"alertgroup"` |  |
| vmstack.alertmanager.config.route.group_by[1] | string | `"job"` |  |
| vmstack.alertmanager.config.route.group_interval | string | `"5m"` |  |
| vmstack.alertmanager.config.route.group_wait | string | `"30s"` |  |
| vmstack.alertmanager.config.route.receiver | string | `"blackhole"` |  |
| vmstack.alertmanager.config.route.repeat_interval | string | `"12h"` |  |
| vmstack.alertmanager.config.route.routes[0].continue | bool | `true` |  |
| vmstack.alertmanager.config.route.routes[0].matchers[0] | string | `"severity=~\"info|warning|critical\""` |  |
| vmstack.alertmanager.config.route.routes[0].receiver | string | `"slack-monitoring"` |  |
| vmstack.alertmanager.enabled | bool | `true` |  |
| vmstack.alertmanager.gafaelfawr.annotations | object | `{}` | Config for the Gafaelfawr ingress to the instance |
| vmstack.alertmanager.gafaelfawr.pathPrefix | string | `"alertmanager"` | Path prefix for web ui |
| vmstack.alertmanager.gafaelfawr.serviceName | string | `"vmalertmanager-victoria-metrics-vmstack"` | The name of the k8s Service to send requests to. These names are created dynamically by the operator. |
| vmstack.alertmanager.monzoTemplate | object | `{"enabled":true}` | Better alert templates for [slack source](https://gist.github.com/milesbxf/e2744fc90e9c41b47aa47925f8ff6512) |
| vmstack.alertmanager.spec.disableNamespaceMatcher | bool | `true` |  |
| vmstack.alertmanager.spec.resources.limits.cpu | string | `"500m"` |  |
| vmstack.alertmanager.spec.resources.limits.memory | string | `"128Mi"` |  |
| vmstack.alertmanager.spec.resources.requests.cpu | string | `"250m"` |  |
| vmstack.alertmanager.spec.resources.requests.memory | string | `"64Mi"` |  |
| vmstack.alertmanager.spec.selectAllByDefault | bool | `true` |  |
| vmstack.alertmanager.spec.storage.volumeClaimTemplate.spec.accessModes[0] | string | `"ReadWriteOnce"` |  |
| vmstack.alertmanager.spec.storage.volumeClaimTemplate.spec.resources.requests.storage | string | `"2Gi"` |  |
| vmstack.alertmanager.spec.storage.volumeClaimTemplate.spec.storageClassName | string | `nil` |  |
| vmstack.alertmanager.spec.useVMConfigReloader | bool | `true` | UseVMConfigReloader replaces prometheus-like config-reloader with vm one. It uses secrets watch instead of file watch which greatly increases speed of config updates |
| vmstack.alertmanager.spec.volumeMounts[0].mountPath | string | `"/etc/alertmanager/slack-config"` |  |
| vmstack.alertmanager.spec.volumeMounts[0].name | string | `"slack-token"` |  |
| vmstack.alertmanager.spec.volumes[0].name | string | `"slack-token"` |  |
| vmstack.alertmanager.spec.volumes[0].secret.items[0].key | string | `"slack-alert-webhook"` |  |
| vmstack.alertmanager.spec.volumes[0].secret.items[0].path | string | `"slack-alert-webhook"` |  |
| vmstack.alertmanager.spec.volumes[0].secret.secretName | string | `"victoria-metrics"` |  |
| vmstack.alertmanager.useManagedConfig | object | `false` | Alertmanager configuration |
| vmstack.coreDns.enabled | bool | `false` |  |
| vmstack.defaultDashboards.dashboards.node-exporter-full.enabled | bool | `false` |  |
| vmstack.defaultDashboards.enabled | bool | `true` |  |
| vmstack.defaultDashboards.grafanaOperator.enabled | bool | `true` |  |
| vmstack.defaultDashboards.grafanaOperator.spec.allowCrossNamespaceImport | bool | `true` |  |
| vmstack.defaultDatasources | object | `{"grafanaOperator":{"enabled":true,"spec":{"allowCrossNamespaceImport":true}}}` | Create grafana datasources for the VictoriaMetrics instance |
| vmstack.defaultDatasources.grafanaOperator.enabled | bool | `true` | Create datasources as CRDs (requires grafana-operator to be installed) |
| vmstack.defaultRules | object | `{"create":true,"groups":{"alertmanager":{"create":true,"rules":{}},"etcd":{"create":false,"rules":{}},"general":{"create":true,"rules":{}},"k8sContainerCpuLimits":{"create":true,"rules":{}},"k8sContainerCpuRequests":{"create":true,"rules":{}},"k8sContainerCpuUsageSecondsTotal":{"create":true,"rules":{}},"k8sContainerMemoryCache":{"create":true,"rules":{}},"k8sContainerMemoryLimits":{"create":true,"rules":{}},"k8sContainerMemoryRequests":{"create":true,"rules":{}},"k8sContainerMemoryRss":{"create":true,"rules":{}},"k8sContainerMemorySwap":{"create":true,"rules":{}},"k8sContainerMemoryWorkingSetBytes":{"create":true,"rules":{}},"k8sContainerResource":{"create":true,"rules":{}},"k8sPodOwner":{"create":true,"rules":{}},"kubeApiserver":{"create":false,"rules":{}},"kubeApiserverAvailability":{"create":false,"rules":{}},"kubeApiserverBurnrate":{"create":false,"rules":{}},"kubeApiserverHistogram":{"create":false,"rules":{}},"kubeApiserverSlos":{"create":false,"rules":{}},"kubePrometheusGeneral":{"create":true,"rules":{}},"kubePrometheusNodeRecording":{"create":false,"rules":{}},"kubeScheduler":{"create":false,"rules":{}},"kubeStateMetrics":{"create":true,"rules":{}},"kubelet":{"create":true,"rules":{}},"kubernetesApps":{"create":true,"rules":{},"targetNamespace":".*"},"kubernetesResources":{"create":true,"rules":{}},"kubernetesStorage":{"create":true,"rules":{},"targetNamespace":".*"},"kubernetesSystem":{"create":true,"rules":{}},"kubernetesSystemApiserver":{"create":false,"rules":{}},"kubernetesSystemControllerManager":{"create":false,"rules":{}},"kubernetesSystemKubelet":{"create":true,"rules":{}},"kubernetesSystemScheduler":{"create":false,"rules":{}},"node":{"create":false,"rules":{}},"nodeNetwork":{"create":false,"rules":{}},"vmHealth":{"create":true,"rules":{}},"vmagent":{"create":true,"rules":{}},"vmcluster":{"create":true,"rules":{}},"vmoperator":{"create":true,"rules":{}},"vmsingle":{"create":true,"rules":{}}}}` | Create default rules for monitoring the cluster |
| vmstack.defaultRules.groups.etcd.rules | object | `{}` | Common properties for all rules in a group |
| vmstack.grafana.enabled | bool | `false` |  |
| vmstack.grafana.forceDeployDatasource | bool | `true` |  |
| vmstack.kube-state-metrics.enabled | bool | `true` |  |
| vmstack.kubeApiServer.enabled | bool | `false` |  |
| vmstack.kubeControllerManager.enabled | bool | `false` |  |
| vmstack.kubeDns.enabled | bool | `false` |  |
| vmstack.kubeEtcd.enabled | bool | `false` |  |
| vmstack.kubeProxy.enabled | bool | `false` |  |
| vmstack.kubeScheduler.enabled | bool | `false` |  |
| vmstack.kubelet.enabled | bool | `true` |  |
| vmstack.kubelet.vmScrape.spec.relabelConfigs[0].action | string | `"labelmap"` |  |
| vmstack.kubelet.vmScrape.spec.relabelConfigs[0].regex | string | `"__meta_kubernetes_node_label_(kubenetes_io_hostname|topology_kubernetes_io_region|topology_kubernetes_io_zone|node_pool|environment|cluster_name|kubernetes_io_instance_type)"` |  |
| vmstack.kubelet.vmScrape.spec.relabelConfigs[1].sourceLabels[0] | string | `"__metrics_path__"` |  |
| vmstack.kubelet.vmScrape.spec.relabelConfigs[1].targetLabel | string | `"metrics_path"` |  |
| vmstack.kubelet.vmScrape.spec.relabelConfigs[2].replacement | string | `"kubelet"` |  |
| vmstack.kubelet.vmScrape.spec.relabelConfigs[2].targetLabel | string | `"job"` |  |
| vmstack.kubelet.vmScrapes.cadvisor.enabled | bool | `true` |  |
| vmstack.kubelet.vmScrapes.probes.enabled | bool | `false` |  |
| vmstack.kubelet.vmScrapes.resources.enabled | bool | `false` |  |
| vmstack.prometheus-node-exporter.enabled | bool | `false` |  |
| vmstack.victoria-metrics-operator | object | see `values.yaml` and [here](https://github.com/VictoriaMetrics/helm-charts/blob/master/charts/victoria-metrics-k8s-stack/values.yaml) | VictoriaMetrics Operator dependency chart configuration. More values can be found [here](https://docs.victoriametrics.com/helm/victoriametrics-operator#parameters). Also checkout [here](https://docs.victoriametrics.com/operator/vars) possible ENV variables to configure operator behaviour |
| vmstack.victoria-metrics-operator.admissionWebhooks.certManager.enabled | bool | `true` | true if cert-manager should manage the validating adminssion webhook cert. Self signed certs are OK here. If possible, it's nice to have cert-manager manage them so that: * They get renewed as needed * The ArgoCD diff doesn't get clogged up with the operator regenerating   them on every sync |
| vmstack.victoria-metrics-operator.env | list | `[{"name":"VM_ENABLESTRICTSECURITY","value":"true"}]` | Extra settings for the operator deployment. Full list [here](https://docs.victoriametrics.com/operator/vars) |
| vmstack.vmCluster.enabled | bool | `false` |  |
| vmstack.vmagent | object | see `values.yaml` and [here](https://github.com/VictoriaMetrics/helm-charts/blob/master/charts/victoria-metrics-k8s-stack/values.yaml) | Configuration for vmagent |
| vmstack.vmagent.gafaelfawr.annotations | object | `{}` | Config for the Gafaelfawr ingress to the instance |
| vmstack.vmagent.gafaelfawr.pathPrefix | string | `"vmagent"` | Path prefix for web ui |
| vmstack.vmagent.gafaelfawr.serviceName | string | `"vmagent-victoria-metrics-vmstack"` | The name of the k8s Service to send requests to. These names are created dynamically by the operator. |
| vmstack.vmagent.spec | object | See `values.yaml` and https://docs.victoriametrics.com/operator/resources/vmagent | Configuration for the VMAgent CRD |
| vmstack.vmagent.spec.statefulMode | bool | `true` | Enable persistence for metrics ingest buffer https://docs.victoriametrics.com/operator/resources/vmagent#statefulmode |
| vmstack.vmagent.spec.statefulStorage | object | `{"volumeClaimTemplate":{"spec":{"accessModes":["ReadWriteOnce"],"resources":{"requests":{"storage":"5Gi"}},"storageClassName":null}}}` | Persistent metrics ingest buffer storage config https://docs.victoriametrics.com/operator/api/#vmagentspec-statefulstorage |
| vmstack.vmalert.enabled | bool | `true` |  |
| vmstack.vmalert.gafaelfawr.annotations | object | `{}` | Config for the Gafaelfawr ingress to the instance |
| vmstack.vmalert.gafaelfawr.pathPrefix | string | `"vmalert"` | Path prefix for web ui |
| vmstack.vmalert.gafaelfawr.serviceName | string | `"vmalert-victoria-metrics-vmstack"` | The name of the k8s Service to send requests to. These names are created dynamically by the operator. |
| vmstack.vmalert.spec.extraArgs."envflag.enable" | string | `"true"` |  |
| vmstack.vmalert.spec.extraEnvsFrom[0].configMapRef.name | string | `"vmagent-extra-args"` |  |
| vmstack.vmauth.enabled | bool | `false` |  |
| vmstack.vmsingle | object | see `values.yaml` and [here](https://github.com/VictoriaMetrics/helm-charts/blob/master/charts/victoria-metrics-k8s-stack/values.yaml) | Configuration for the VictoriaMetrics [VMSingle instance](https://docs.victoriametrics.com/operator/resources/vmsingle/) |
| vmstack.vmsingle.gafaelfawr.annotations | object | `{}` | Config for the Gafaelfawr ingress to instance |
| vmstack.vmsingle.gafaelfawr.pathPrefix | string | `"vm"` | Path prefix for web ui |
| vmstack.vmsingle.gafaelfawr.serviceName | string | `"vmsingle-victoria-metrics-vmstack"` | The name of the k8s Service to send requests to. These names are created dynamically by the operator. |
| vmstack.vmsingle.spec | object | See `values.yaml` | Full spec for VMSingle CRD. Allowed values describe [here](https://docs.victoriametrics.com/operator/api#vmsinglespec) |
| vmstack.vmsingle.spec.removePvcAfterDelete | bool | `false` | if true, controller adds ownership to pvc and after VMSingle object deletion - pvc will be garbage collected by controller manager |
| vmstack.vmsingle.spec.retentionPeriod | string | `"30d"` | The amount of time to retain data. Takes a number followed by a time unit character - h(ours), d(ays), w(eeks), y(ears). If the time unit is not specified, a month (31 days) is assumed. |
| vmstack.vmsingle.spec.storage | object | `{"accessModes":["ReadWriteOnce"],"resources":{"requests":{"storage":"10Gi"}},"storageClassName":null}` | The definition of how storage will be used by the VMSingle  Schema is a Kubernetes PersistentVolumeClaim spec. https://docs.victoriametrics.com/operator/api#vmsinglespec-storage |
