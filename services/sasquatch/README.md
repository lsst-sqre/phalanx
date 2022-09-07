# sasquatch

Rubin Observatory's telemetry service.

## Requirements

| Repository | Name | Version |
|------------|------|---------|
|  | kafdrop | 1.0.0 |
|  | kafka-connect-manager | 1.0.0 |
|  | strimzi-kafka | 1.0.0 |
| https://helm.influxdata.com/ | chronograf | 1.2.5 |
| https://helm.influxdata.com/ | influxdb | 4.12.0 |
| https://helm.influxdata.com/ | kapacitor | 1.4.6 |
| https://lsst-sqre.github.io/charts/ | strimzi-registry-operator | 2.1.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| chronograf.env | object | `{"BASE_PATH":"/chronograf","CUSTOM_AUTO_REFRESH":"1s=1000","HOST_PAGE_DISABLED":true}` | Chronograf environment variables. |
| chronograf.envFromSecret | string | `"sasquatch"` | Chronograf secrets, expected keys generic_client_id, generic_client_secret and token_secret. |
| chronograf.image | object | `{"repository":"quay.io/influxdb/chronograf","tag":"1.9.4"}` | Chronograf image tag. |
| chronograf.ingress | object | disabled | Chronograf ingress configuration. |
| chronograf.persistence | object | `{"enabled":true,"size":"100Gi"}` | Chronograf data persistence configuration. |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| influxdb.config | object | `{"continuous_queries":{"enabled":false},"coordinator":{"log-queries-after":"15s","max-concurrent-queries":0,"query-timeout":"0s","write-timeout":"1h"},"data":{"cache-max-memory-size":0,"trace-logging-enabled":true,"wal-fsync-delay":"100ms"},"http":{"auth-enabled":true,"enabled":true,"flux-enabled":true,"max-row-limit":0},"logging":{"level":"debug"}}` | Override InfluxDB configuration. See https://docs.influxdata.com/influxdb/v1.8/administration/config |
| influxdb.image | object | `{"tag":"1.8.10"}` | InfluxDB image tag. |
| influxdb.ingress | object | disabled | InfluxDB ingress configuration. |
| influxdb.initScripts.enabled | bool | `false` | Enable InfluxDB custom initialization script. |
| influxdb.persistence.enabled | bool | `true` | Enable persistent volume claim. By default storageClass is undefined choosing the default provisioner (standard on GKE). |
| influxdb.persistence.size | string | `"1Ti"` | Persistent volume size. @default 1Ti for teststand deployments |
| influxdb.setDefaultUser | object | `{"enabled":true,"user":{"existingSecret":"sasquatch"}}` | Default InfluxDB user, use influxb-user and influxdb-password keys from secret. |
| kafka-connect-manager | object | `{}` | Override kafka-connect-manager configuration. |
| kapacitor.envVars | object | `{"KAPACITOR_SLACK_ENABLED":true}` | Kapacitor environment variables. |
| kapacitor.existingSecret | string | `"sasquatch"` | InfluxDB credentials, use influxdb-user and influxdb-password keys from secret. |
| kapacitor.image | object | `{"repository":"kapacitor","tag":"1.6.5"}` | Kapacitor image tag. |
| kapacitor.influxURL | string | `"http://sasquatch-influxdb.sasquatch:8086"` | InfluxDB connection URL. |
| kapacitor.persistence | object | `{"enabled":true,"size":"100Gi"}` | Chronograf data persistence configuration. |
| kapacitor.resources.limits.cpu | int | `4` |  |
| kapacitor.resources.limits.memory | string | `"16Gi"` |  |
| kapacitor.resources.requests.cpu | int | `1` |  |
| kapacitor.resources.requests.memory | string | `"1Gi"` |  |
| strimzi-kafka | object | `{}` | Override strimzi-kafka configuration. |
| strimzi-registry-operator | object | `{"clusterName":"sasquatch","clusterNamespace":"sasquatch","operatorNamespace":"sasquatch"}` | strimzi-registry-operator configuration. |
