# sasquatch

Rubin Observatory's telemetry service.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| bucketmapper.image | object | `{"repository":"ghcr.io/lsst-sqre/rubin-influx-tools","tag":"0.1.23"}` | image for monitoring-related cronjobs |
| bucketmapper.image.repository | string | `"ghcr.io/lsst-sqre/rubin-influx-tools"` | repository for rubin-influx-tools |
| bucketmapper.image.tag | string | `"0.1.23"` | tag for rubin-influx-tools |
| chronograf.enabled | bool | `true` | Enable Chronograf. |
| chronograf.env | object | `{"BASE_PATH":"/chronograf","CUSTOM_AUTO_REFRESH":"1s=1000","HOST_PAGE_DISABLED":true}` | Chronograf environment variables. |
| chronograf.envFromSecret | string | `"sasquatch"` | Chronograf secrets, expected keys generic_client_id, generic_client_secret and token_secret. |
| chronograf.image | object | `{"repository":"quay.io/influxdb/chronograf","tag":"1.9.4"}` | Chronograf image tag. |
| chronograf.ingress | object | disabled | Chronograf ingress configuration. |
| chronograf.persistence | object | `{"enabled":true,"size":"100Gi"}` | Chronograf data persistence configuration. |
| chronograf.resources.limits.cpu | int | `4` |  |
| chronograf.resources.limits.memory | string | `"16Gi"` |  |
| chronograf.resources.requests.cpu | int | `1` |  |
| chronograf.resources.requests.memory | string | `"1Gi"` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| influxdb.config | object | `{"continuous_queries":{"enabled":false},"coordinator":{"log-queries-after":"15s","max-concurrent-queries":0,"query-timeout":"0s","write-timeout":"1h"},"data":{"cache-max-memory-size":0,"trace-logging-enabled":true,"wal-fsync-delay":"100ms"},"http":{"auth-enabled":true,"enabled":true,"flux-enabled":true,"max-row-limit":0},"logging":{"level":"debug"}}` | Override InfluxDB configuration. See https://docs.influxdata.com/influxdb/v1.8/administration/config |
| influxdb.enabled | bool | `true` | Enable InfluxDB. |
| influxdb.image | object | `{"tag":"1.8.10"}` | InfluxDB image tag. |
| influxdb.ingress | object | disabled | InfluxDB ingress configuration. |
| influxdb.initScripts.enabled | bool | `false` | Enable InfluxDB custom initialization script. |
| influxdb.persistence.enabled | bool | `true` | Enable persistent volume claim. By default storageClass is undefined choosing the default provisioner (standard on GKE). |
| influxdb.persistence.size | string | `"1Ti"` | Persistent volume size. @default 1Ti for teststand deployments |
| influxdb.resources.limits.cpu | int | `8` |  |
| influxdb.resources.limits.memory | string | `"96Gi"` |  |
| influxdb.resources.requests.cpu | int | `1` |  |
| influxdb.resources.requests.memory | string | `"1Gi"` |  |
| influxdb.setDefaultUser | object | `{"enabled":true,"user":{"existingSecret":"sasquatch"}}` | Default InfluxDB user, use influxb-user and influxdb-password keys from secret. |
| influxdb2.adminUser.bucket | string | `"default"` | Admin default bucket. |
| influxdb2.adminUser.existingSecret | string | `"sasquatch"` | Get admin-password/admin-token keys from secret. |
| influxdb2.adminUser.organization | string | `"default"` | Admin default organization. |
| influxdb2.enabled | bool | `false` |  |
| influxdb2.env[0].name | string | `"INFLUXD_STORAGE_WAL_FSYNC_DELAY"` |  |
| influxdb2.env[0].value | string | `"100ms"` |  |
| influxdb2.env[1].name | string | `"INFLUXD_HTTP_IDLE_TIMEOUT"` |  |
| influxdb2.env[1].value | string | `"0"` |  |
| influxdb2.env[2].name | string | `"INFLUXD_FLUX_LOG_ENABLED"` |  |
| influxdb2.env[2].value | string | `"true"` |  |
| influxdb2.env[3].name | string | `"INFLUXD_LOG_LEVEL"` |  |
| influxdb2.env[3].value | string | `"debug"` |  |
| influxdb2.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/api/v2/$2"` |  |
| influxdb2.ingress.className | string | `"nginx"` |  |
| influxdb2.ingress.enabled | bool | `false` | InfluxDB2 ingress configuration |
| influxdb2.ingress.hostname | string | `""` |  |
| influxdb2.ingress.path | string | `"/influxdb2(/|$)(.*)"` |  |
| influxdb2.initScripts.enabled | bool | `true` | InfluxDB2 initialization scripts |
| influxdb2.initScripts.scripts."init.sh" | string | `"#!/bin/bash\ninflux bucket create --name telegraf-kafka-consumer --org default\n"` |  |
| influxdb2.persistence.enabled | bool | `true` | Enable persistent volume claim. By default storageClass is undefined choosing the default provisioner (standard on GKE). |
| influxdb2.persistence.size | string | `"1Ti"` | Persistent volume size. @default 1Ti for teststand deployments. |
| influxdb2.resources.limits.cpu | int | `8` |  |
| influxdb2.resources.limits.memory | string | `"96Gi"` |  |
| influxdb2.resources.requests.cpu | int | `1` |  |
| influxdb2.resources.requests.memory | string | `"1Gi"` |  |
| kafdrop.enabled | bool | `true` | Enable Kafdrop. |
| kafka-connect-manager | object | `{}` | Override kafka-connect-manager configuration. |
| kapacitor.enabled | bool | `true` | Enable Kapacitor. |
| kapacitor.envVars | object | `{"KAPACITOR_SLACK_ENABLED":true}` | Kapacitor environment variables. |
| kapacitor.existingSecret | string | `"sasquatch"` | InfluxDB credentials, use influxdb-user and influxdb-password keys from secret. |
| kapacitor.image | object | `{"repository":"kapacitor","tag":"1.6.6"}` | Kapacitor image tag. |
| kapacitor.influxURL | string | `"http://sasquatch-influxdb.sasquatch:8086"` | InfluxDB connection URL. |
| kapacitor.persistence | object | `{"enabled":true,"size":"100Gi"}` | Chronograf data persistence configuration. |
| kapacitor.resources.limits.cpu | int | `4` |  |
| kapacitor.resources.limits.memory | string | `"16Gi"` |  |
| kapacitor.resources.requests.cpu | int | `1` |  |
| kapacitor.resources.requests.memory | string | `"1Gi"` |  |
| rest-proxy | object | `{"enabled":false}` | Override rest-proxy configuration. |
| strimzi-kafka | object | `{}` | Override strimzi-kafka configuration. |
| strimzi-registry-operator | object | `{"clusterName":"sasquatch","clusterNamespace":"sasquatch","operatorNamespace":"sasquatch"}` | strimzi-registry-operator configuration. |
| telegraf-kafka-consumer | object | `{"enabled":false}` | Override telegraf-kafka-consumer configuration. |
