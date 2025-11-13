# keda

Kubernetes Event Driven Autoscaling

## Source Code

* <https://github.com/kedacore/charts/blob/main/keda/values.yaml>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| keda.affinity | object | `{}` | [Affinity] for pod scheduling for KEDA operator, Metrics API Server and KEDA admission webhooks. |
| keda.enableServiceLinks | bool | `false` | Enable service links in pods. Although enabled, mirroring k8s default, it is highly recommended to disable, due to its legacy status [Legacy container links](https://docs.docker.com/engine/network/links/) |
| keda.logging.metricServer.level | int | `0` | Logging level for Metrics Server. allowed values: `0` for info, `4` for debug, or an integer value greater than 0, specified as string |
| keda.logging.metricServer.stderrthreshold | string | `"ERROR"` | Logging stderrthreshold for Metrics Server allowed values: 'DEBUG','INFO','WARN','ERROR','ALERT','EMERG' |
| keda.logging.operator.format | string | `"console"` | Logging format for KEDA Operator. allowed values: `json` or `console` |
| keda.logging.operator.level | string | `"info"` | Logging level for KEDA Operator. allowed values: `debug`, `info`, `error`, or an integer value greater than 0, specified as string |
| keda.logging.operator.stackTracesEnabled | bool | `false` | If enabled, the stack traces will be also printed |
| keda.logging.operator.timeEncoding | string | `"rfc3339"` | Logging time encoding for KEDA Operator. allowed values are `epoch`, `millis`, `nano`, `iso8601`, `rfc3339` or `rfc3339nano` |
| keda.nodeSelector | object | `{}` | Node selector for pod scheduling ([docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)) |
| keda.priorityClassName | string | `""` | priorityClassName for all KEDA components |
| keda.prometheus.metricServer.enabled | bool | `true` | Enable metric server Prometheus metrics expose |
| keda.prometheus.metricServer.port | int | `8000` | HTTP port used for exposing metrics server prometheus metrics |
| keda.prometheus.operator.enabled | bool | `true` | Enable KEDA Operator prometheus metrics expose |
| keda.prometheus.operator.port | int | `8000` | Port used for exposing KEDA Operator prometheus metrics |
| keda.resources.metricServer | object | `{"limits":{"cpu":1,"memory":"1000Mi"},"requests":{"cpu":"100m","memory":"100Mi"}}` | Manage [resource request & limits] of KEDA metrics apiserver pod |
| keda.resources.operator | object | `{"limits":{"cpu":1,"memory":"1000Mi"},"requests":{"cpu":"100m","memory":"100Mi"}}` | Manage [resource request & limits] of KEDA operator pod |
| keda.resources.webhooks | object | `{"limits":{"cpu":1,"memory":"1000Mi"},"requests":{"cpu":"100m","memory":"100Mi"}}` | Manage [resource request & limits] of KEDA admission webhooks pod |
| keda.tolerations | list | `[]` | Tolerations for pod scheduling ([docs](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)) |
| keda.topologySpreadConstraints.metricsServer | list | `[]` | [Pod Topology Constraints] of KEDA metrics apiserver pod |
| keda.topologySpreadConstraints.operator | list | `[]` | [Pod Topology Constraints] of KEDA operator pod |
| keda.topologySpreadConstraints.webhooks | list | `[]` | [Pod Topology Constraints] of KEDA admission webhooks pod |
| keda.watchNamespace | string | `""` | Defines Kubernetes namespaces to watch to scale their workloads. Default watches all namespaces |
