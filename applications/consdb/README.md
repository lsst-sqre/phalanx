# consdb

Consolidated Database of Image Metadata

**Homepage:** <https://consdb.lsst.io/>

## Source Code

* <https://github.com/lsst-dm/consdb>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the consdb deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of consdb deployment |
| autoscaling.maxReplicas | int | `10` | Maximum number of consdb deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of consdb deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of consdb deployment pods |
| db.database | string | `"consdb"` | Database name |
| db.host | string | `"postgres.postgres"` | Database host |
| db.user | string | `"consdb"` | Database user |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| hinfo.image.pullPolicy | string | `"Always"` | Pull policy for the consdb-hinfo image |
| hinfo.image.repository | string | `"ghcr.io/lsst-dm/consdb-hinfo"` | Image to use in the consdb-hinfo deployment |
| hinfo.latiss.enable | bool | `false` | Enable deployment of consdb-hinfo for LATISS. |
| hinfo.latiss.logConfig | string | `"INFO"` | Log configuration for LATISS deployment. |
| hinfo.latiss.tag | string | `""` | Tag for LATISS deployment. |
| hinfo.lsstcam.enable | bool | `false` | Enable deployment of consdb-hinfo for LSSTCam. |
| hinfo.lsstcam.logConfig | string | `"INFO"` | Log configuration for LSSTCam deployment. |
| hinfo.lsstcam.tag | string | `""` | Tag for LSSTCam deployment. |
| hinfo.lsstcomcam.enable | bool | `false` | Enable deployment of consdb-hinfo for LSSTComCam. |
| hinfo.lsstcomcam.logConfig | string | `"INFO"` | Log configuration for LSSTComCam deployment. |
| hinfo.lsstcomcam.tag | string | `""` | Tag for LSSTComCam deployment. |
| hinfo.replicaCount | int | `1` | Number of consdb-hinfo deployment pods to start per instrument |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| kafka.bootstrap | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka bootstrap server |
| kafka.group_id | string | `"consdb-consumer"` | Name of Kafka consumer group |
| kafka.schema_url | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Kafka Avro schema server URL |
| kafka.username | string | `"consdb"` | Username for SASL_PLAIN authentication |
| lfa.access_key | string | `""` | Access key for LFA bucket |
| lfa.bucket_prefix | string | `""` | Prefix for LFA bucket (e.g. for Ceph tenant specification) |
| lfa.s3EndpointUrl | string | `""` | url |
| nodeSelector | object | `{}` | Node selection rules for the consdb deployment pod |
| podAnnotations | object | `{}` | Annotations for the consdb deployment pod |
| pq.image.pullPolicy | string | `"Always"` | Pull policy for the consdb-hinfo image |
| pq.image.repository | string | `"ghcr.io/lsst-dm/consdb-pq"` | Image to use in the consdb-pq deployment |
| pq.image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| pq.replicaCount | int | `1` | Number of consdb-hinfo deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the consdb deployment pod |
| tolerations | list | `[]` | Tolerations for the consdb deployment pod |
