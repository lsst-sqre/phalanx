# app-metrics

Kafka topics, users, and a telegraf connector for metrics events.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity for pod assignment |
| apps | list | `[]` | A list of applications that will publish metrics events, and the keys that should be ingested into InfluxDB as tags.  The names should be the same as the app names in Phalanx. |
| args | list | `[]` | Arguments passed to the Telegraf agent containers |
| cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| debug | bool | false | Run Telegraf in debug mode. |
| env | list | See `values.yaml` | Telegraf agent enviroment variables |
| envFromSecret | string | `""` | Name of the secret with values to be added to the environment |
| globalAppConfig | object | See `values.yaml` | app-metrics configuration in any environment in which the subchart is enabled. This should stay globally specified here, and it shouldn't be overridden.  See [here](https://sasquatch.lsst.io/user-guide/app-metrics.html#configuration) for the structure of this value. |
| globalInfluxTags | list | `["application"]` | Keys in an every event sent by any app that should be recorded in InfluxDB as "tags" (vs. "fields"). These will be concatenated with the `influxTags` from `globalAppConfig` |
| image.pullPolicy | string | `"Always"` | Image pull policy |
| image.repo | string | `"ghcr.io/lsst-sqre/telegraf"` | Telegraf image repository |
| image.tag | string | `"nightly-alpine-2025-01-09"` | Telegraf image tag |
| imagePullSecrets | list | `[]` | Secret names to use for Docker pulls |
| influxdb.url | string | `"http://sasquatch-influxdb.sasquatch:8086"` | URL of the InfluxDB v1 instance to write to |
| nodeSelector | object | `{}` | Node labels for pod assignment |
| podAnnotations | object | `{}` | Annotations for telegraf-kafka-consumers pods |
| podLabels | object | `{}` | Labels for telegraf-kafka-consumer pods |
| replicaCount | int | `3` | Number of Telegraf replicas. Multiple replicas increase availability. |
| resources | object | See `values.yaml` | Kubernetes resources requests and limits |
| tolerations | list | `[]` | Tolerations for pod assignment |
