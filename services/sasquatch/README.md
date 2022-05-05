# sasquatch

Rubin Observatory's telemetry service.

## Requirements

| Repository | Name | Version |
|------------|------|---------|
|  | kafka-connect-manager | 1.0.0 |
|  | strimzi-kafka | 1.0.0 |
| https://helm.influxdata.com/ | chronograf | 1.2.5 |
| https://helm.influxdata.com/ | influxdb | 4.11.0 |
| https://helm.influxdata.com/ | kapacitor | 1.4.6 |
| https://helm.influxdata.com/ | telegraf | 1.8.18 |
| https://lsst-sqre.github.io/charts/ | strimzi-registry-operator | 1.2.0 |
| https://lsst-ts.github.io/charts/ | csc | 0.9.2 |
| https://lsst-ts.github.io/charts/ | kafka-producers | 0.10.1 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| chronograf.env | object | `{"BASE_PATH":"/chronograf","CUSTOM_AUTO_REFRESH":"1s=1000","HOST_PAGE_DISABLED":true}` | Chronograf environment variables. |
| chronograf.envFromSecret | string | `"sasquatch"` | Chronograf secrets, expected keys generic_client_id, generic_client_secret and token_secret. |
| chronograf.image | object | `{"repository":"quay.io/influxdb/chronograf","tag":"1.9.4"}` | Chronograf image tag. |
| chronograf.ingress | object | disabled | Chronograf ingress configuration. |
| chronograf.persistence | object | `{"enabled":true,"size":"16Gi"}` | Chronograf data persistence configuration. |
| csc.enabled | bool | `false` | Whether the test csc is deployed. |
| csc.env | object | `{"LSST_DDS_PARTITION_PREFIX":"test","LSST_SITE":"test","OSPL_ERRORFILE":"/tmp/ospl-error-test.log","OSPL_INFOFILE":"/tmp/ospl-info-test.log","OSPL_URI":"file:///opt/lsst/software/stack/miniconda/lib/python3.8/config/ospl-std.xml"}` | Enviroment variables to run the Test CSC. |
| csc.env.OSPL_URI | string | `"file:///opt/lsst/software/stack/miniconda/lib/python3.8/config/ospl-std.xml"` | Use a single process configuration for DDS OpenSplice. |
| csc.image.nexus3 | string | `"nexus3-docker"` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled. |
| csc.image.repository | string | `"ts-dockerhub.lsst.org/test"` | The Docker registry name of the container image to use for the CSC |
| csc.image.tag | string | `"c0025"` | The tag of the container image to use for the CSC |
| csc.namespace | string | `"sasquatch"` | Namespace where the Test CSC is deployed. |
| csc.osplVersion | string | `"V6.10.4"` | DDS OpenSplice version. |
| csc.useExternalConfig | bool | `false` | Wether to use an external configuration for DDS OpenSplice. |
| influxdb.config | object | `{"continuous_queries":{"enabled":false},"coordinator":{"log-queries-after":"15s","max-concurrent-queries":10,"query-timeout":"900s","write-timeout":"60s"},"data":{"cache-max-memory-size":0,"trace-logging-enabled":true,"wal-fsync-delay":"100ms"},"http":{"auth-enabled":true,"enabled":true,"flux-enabled":true,"max-row-limit":0}}` | Override InfluxDB configuration. See https://docs.influxdata.com/influxdb/v1.8/administration/config |
| influxdb.image | object | `{"tag":"1.8.10"}` | InfluxDB image tag. |
| influxdb.ingress | object | disabled | InfluxDB ingress configuration. |
| influxdb.initScripts | object | `{"enabled":true,"scripts":{"init.iql":"CREATE DATABASE \"telegraf\" WITH DURATION 30d REPLICATION 1 NAME \"rp_30d\"\n\n"}}` | InfluxDB Custom initialization scripts. |
| influxdb.setDefaultUser | object | `{"enabled":true,"user":{"existingSecret":"sasquatch"}}` | Default InfluxDB user, use influxb-user and influxdb-password keys from secret. |
| kafka-connect-manager | object | `{}` | Override strimzi-kafka configuration. |
| kafka-producers.enabled | bool | `false` | Whether the kafka-producer for the test csc is deployed. |
| kafka-producers.env.brokerIp | string | `"sasquatch-kafka-bootstrap.sasquatch"` | The URI for the Sasquatch Kafka broker. |
| kafka-producers.env.brokerPort | int | `9092` | The port for the Sasquatch Kafka listener. |
| kafka-producers.env.extras.LSST_DDS_RESPONSIVENESS_TIMEOUT | string | `"15s"` |  |
| kafka-producers.env.extras.OSPL_ERRORFILE | string | `"/tmp/ospl-error-kafka-producers.log"` |  |
| kafka-producers.env.extras.OSPL_INFOFILE | string | `"/tmp/ospl-info-kafka-producers.log"` |  |
| kafka-producers.env.extras.OSPL_URI | string | `"file:///opt/lsst/software/stack/miniconda/lib/python3.8/config/ospl-std.xml"` | Use a single process configuration for DDS OpenSplice. |
| kafka-producers.env.logLevel | int | `20` | Logging level for the Kafka producers |
| kafka-producers.env.lsstDdsPartitionPrefix | string | `"test"` | The LSST_DDS_PARTITION_PREFIX name applied to all producer containers. |
| kafka-producers.env.registryAddr | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | The Sasquatch Schema Registry URL. |
| kafka-producers.env.replication | int | `3` | The topic replication factor (should be the same as the number of Kafka broker in Sasquatch) |
| kafka-producers.image.nexus3 | string | `"nexus3-docker"` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled. |
| kafka-producers.image.repository | string | `"ts-dockerhub.lsst.org/salkafka"` | The Docker registry name of the container image to use for the producers. |
| kafka-producers.image.tag | string | `"c0025"` | The tag of the container image to use for the producers. |
| kafka-producers.namespace | string | `"sasquatch"` | Namespace where the Test CSC is deployed. |
| kafka-producers.osplVersion | string | `"V6.10.4"` | DDS OpenSplice version. |
| kafka-producers.producers | object | `{"test":{"cscs":"Test"}}` | List of producers and CSCs to get DDS samples from. |
| kafka-producers.startupProbe.failureThreshold | int | `15` | The number of times the startup probe is allowed to fail before failing the probe |
| kafka-producers.startupProbe.initialDelay | int | `20` | The initial delay in seconds before the first check is made |
| kafka-producers.startupProbe.period | int | `10` | The time in seconds between subsequent checks |
| kafka-producers.startupProbe.use | bool | `true` | Whether to use the startup probe |
| kafka-producers.useExternalConfig | bool | `false` | Wether to use an external configuration for DDS OpenSplice. |
| kapacitor.envVars | object | `{"KAPACITOR_SLACK_ENABLED":true}` | Kapacitor environment variables. |
| kapacitor.existingSecret | string | `"sasquatch"` | InfluxDB credentials, use influxdb-user and influxdb-password keys from secret. |
| kapacitor.image | object | `{"repository":"kapacitor","tag":"1.6.4"}` | Kapacitor image tag. |
| kapacitor.influxURL | string | `"http://sasquatch.influxdb:8086"` | InfluxDB connection URL. |
| kapacitor.persistence | object | `{"enabled":true,"size":"16Gi"}` | Chronograf data persistence configuration. |
| strimzi-kafka | object | `{}` | Override strimzi-kafka configuration. |
| strimzi-registry-operator | object | `{"clusterName":"sasquatch","operatorNamespace":"sasquatch","watchNamespace":"sasquatch"}` | strimzi-registry-operator configuration. |
| telegraf.config.inputs | list | `[{"prometheus":{"metric_version":2,"urls":["http://hub.nublado2:8081/nb/hub/metrics"]}}]` | Telegraf input plugins. Collect JupyterHub Prometheus metrics by dedault. See https://jupyterhub.readthedocs.io/en/stable/reference/metrics.html |
| telegraf.config.outputs | list | `[{"influxdb":{"database":"telegraf","password":"$TELEGRAF_PASSWORD","urls":["http://sasquatch-influxdb.sasquatch:8086"],"username":"telegraf"}}]` | Telegraf default output destination. |
| telegraf.config.processors | object | `{}` | Telegraf processor plugins. |
| telegraf.env[0] | object | `{"name":"TELEGRAF_PASSWORD","valueFrom":{"secretKeyRef":{"key":"telegraf-password","name":"sasquatch"}}}` | Telegraf password. |
| telegraf.podLabels | object | `{"hub.jupyter.org/network-access-hub":"true"}` | Allow network access to JupyterHub pod. |
| telegraf.service.enabled | bool | `false` | Telegraf service. |
| vaultSecretsPath | string | None, must be set | Path to the Vault secrets (`secret/k8s_operator/<hostname>/sasquatch`) |
