# calsys

Deployment for the Calibration System CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| csc_collector | object | `{"secrets":[]}` | The default image tag for all of the child applications imageTag: "" |
| csc_collector.secrets | list | `[]` | This section holds secret specifications. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the secret) _key_ (The key in the vault store where the secret resides) _type_ (OPTIONAL: The secret type. Defaults to Opaque.) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.controlSystemImageTag | string | Set by ArgoCD | Image tag for the control system deployment |
| global.controlSystemKafkaBrokerAddress | string | Set by ArgoCD | Kafka broker address for the control system deployment |
| global.controlSystemS3EndpointUrl | string | Set by ArgoCD | S3 endpoint (LFA) for the control system deployment |
| global.controlSystemSchemaRegistryUrl | string | Set by ArgoCD | Schema registry URL for the control system deployment |
| global.controlSystemSiteTag | string | Set by ArgoCD | Site tag for the control system deployment |
| global.controlSystemTopicName | string | Set by ArgoCD | Topic name tag for the control system deployment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| namespace | string | `""` |  |
