# obsloctap

Publish observing schedule

## Source Code

* <https://github.com/lsst-dm/obsloctap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.obsplanLimit | int | `1000` | limit for obsplan query |
| config.obsplanTimeSpan | int | `24` | time span, if a time is provided in the query how man hours to look back |
| config.persistentVolumeClaims | list | `[]` | PersistentVolumeClaims to create. |
| config.separateSecrets | bool | `true` | Whether to use the new secrets management scheme |
| config.volume_mounts | list | `[]` | Mount points for additional volumes |
| config.volumes | list | `[]` | Additional volumes to attach |
| consumekafka.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsloctap image |
| consumekafka.image.repository | string | `"ghcr.io/lsst-dm/consume-kafka"` | obsloctap image to use |
| consumekafka.image.tag | string | The appVersion of the chart | Tag of image to use |
| environment | object | `{}` | Environment variables (e.g. butler configuration/auth parms) for panel |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| kafka.bootstrap | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka bootstrap server |
| kafka.group_id | string | `"obsloctap-consumer"` | Name of Kafka consumer group |
| kafka.schema_url | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Kafka Avro schema server URL |
| kafka.username | string | `"obsloctap"` | Username for SASL_PLAIN authentication |
| lfa.access_key | string | `""` | Access key for LFA bucket |
| lfa.bucket_prefix | string | `""` | Prefix for LFA bucket (e.g. for Ceph tenant specification) |
| lfa.s3EndpointUrl | string | `""` | url |
| obsloctap.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsloctap image |
| obsloctap.image.repository | string | `"ghcr.io/lsst-dm/obsloctap"` | obsloctap image to use |
| obsloctap.image.tag | string | The appVersion of the chart | Tag of image to use |
