# keda

Kubernetes Event Driven Autoscaling

## Source Code

* <https://github.com/kedacore/charts/blob/main/keda/values.yaml>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | [Affinity] for pod scheduling for KEDA operator, Metrics API Server and KEDA admission webhooks. |
| enableServiceLinks | bool | `false` | Enable service links in pods. Although enabled, mirroring k8s default, it is highly recommended to disable, due to its legacy status [Legacy container links](https://docs.docker.com/engine/network/links/) |
| logging.metricServer.level | int | `0` | Logging level for Metrics Server. allowed values: `0` for info, `4` for debug, or an integer value greater than 0, specified as string |
| logging.metricServer.stderrthreshold | string | `"ERROR"` | Logging stderrthreshold for Metrics Server allowed values: 'DEBUG','INFO','WARN','ERROR','ALERT','EMERG' |
| logging.operator.format | string | `"console"` | Logging format for KEDA Operator. allowed values: `json` or `console` |
| logging.operator.level | string | `"info"` | Logging level for KEDA Operator. allowed values: `debug`, `info`, `error`, or an integer value greater than 0, specified as string |
| logging.operator.stackTracesEnabled | bool | `false` | If enabled, the stack traces will be also printed |
| logging.operator.timeEncoding | string | `"rfc3339"` | Logging time encoding for KEDA Operator. allowed values are `epoch`, `millis`, `nano`, `iso8601`, `rfc3339` or `rfc3339nano` |
| nodeSelector | object | `{}` | Node selector for pod scheduling ([docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)) |
| priorityClassName | string | `""` | priorityClassName for all KEDA components |
| prometheus.metricServer.enabled | bool | `true` | Enable metric server Prometheus metrics expose |
| prometheus.metricServer.port | int | `8000` | HTTP port used for exposing metrics server prometheus metrics |
| prometheus.operator.enabled | bool | `true` | Enable KEDA Operator prometheus metrics expose |
| prometheus.operator.port | int | `8000` | Port used for exposing KEDA Operator prometheus metrics |
| resources.metricServer | object | `{"limits":{"cpu":1,"memory":"1000Mi"},"requests":{"cpu":"100m","memory":"100Mi"}}` | Manage [resource request & limits] of KEDA metrics apiserver pod |
| resources.operator | object | `{"limits":{"cpu":1,"memory":"1000Mi"},"requests":{"cpu":"100m","memory":"100Mi"}}` | Manage [resource request & limits] of KEDA operator pod |
| resources.webhooks | object | `{"limits":{"cpu":1,"memory":"1000Mi"},"requests":{"cpu":"100m","memory":"100Mi"}}` | Manage [resource request & limits] of KEDA admission webhooks pod |
| tolerations | list | `[]` | Tolerations for pod scheduling ([docs](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)) |
| topologySpreadConstraints.metricsServer | list | `[]` | [Pod Topology Constraints] of KEDA metrics apiserver pod |
| topologySpreadConstraints.operator | list | `[]` | [Pod Topology Constraints] of KEDA operator pod |
| topologySpreadConstraints.webhooks | list | `[]` | [Pod Topology Constraints] of KEDA admission webhooks pod |
| watchNamespace | string | `""` | Defines Kubernetes namespaces to watch to scale their workloads. Default watches all namespaces |
