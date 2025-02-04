# obssys

Deployment for the Observatory System CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| gis.enabled | bool | `false` | Enable the GIS CSC |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.controlSystem.appNamespace | string | Set by ArgoCD | Application namespace for the control system deployment |
| global.controlSystem.imageTag | string | Set by ArgoCD | Image tag for the control system deployment |
| global.controlSystem.kafkaBrokerAddress | string | Set by ArgoCD | Kafka broker address for the control system deployment |
| global.controlSystem.kafkaTopicReplicationFactor | string | Set by ArgoCD | Kafka topic replication factor for control system topics |
| global.controlSystem.s3EndpointUrl | string | Set by ArgoCD | S3 endpoint (LFA) for the control system deployment |
| global.controlSystem.schemaRegistryUrl | string | Set by ArgoCD | Schema registry URL for the control system deployment |
| global.controlSystem.siteTag | string | Set by ArgoCD | Site tag for the control system deployment |
| global.controlSystem.topicName | string | Set by ArgoCD | Topic name tag for the control system deployment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
