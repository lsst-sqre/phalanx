# eas

Deployment for the Environmental Awareness Systems CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| auxtel-ess01-sim.enabled | bool | `false` | Enable the ESS:201 simulator CSC |
| auxtel-ess01.enabled | bool | `false` | Enable the ESS:201 CSC |
| auxtel-ess02-sim.enabled | bool | `false` | Enable the ESS:202 simulator CSC |
| auxtel-ess02.enabled | bool | `false` | Enable the ESS:202 CSC |
| auxtel-ess03-sim.enabled | bool | `false` | Enable the ESS:203 simulator CSC |
| auxtel-ess03.enabled | bool | `false` | Enable the ESS:203 CSC |
| auxtel-ess04-sim.enabled | bool | `false` | Enable the ESS:204 simulator CSC |
| auxtel-ess04.enabled | bool | `false` | Enable the ESS:204 CSC |
| auxtel-ess05-sim.enabled | bool | `false` | Enable the ESS:205 simulator CSC |
| auxtel-ess05.enabled | bool | `false` | Enable the ESS:205 CSC |
| calibhill-ess01-sim.enabled | bool | `false` | Enable the ESS:301 simulator CSC |
| calibhill-ess01.enabled | bool | `false` | Enable the ESS:301 CSC |
| csc_shared.pullSecrets | list | `[]` | This section holds pull secret specifications. NOTE: The pull secret is expected to be part of the pull-secret key in Vault. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the pull secret) |
| dimm1-sim.enabled | bool | `false` | Enable the DIMM:1 simulator CSC |
| dimm1.enabled | bool | `false` | Enable the DIMM:1 CSC |
| dimm2-sim.enabled | bool | `false` | Enable the DIMM:2 simulator CSC |
| dimm2.enabled | bool | `false` | Enable the DIMM:2 CSC |
| dsm1-sim.enabled | bool | `false` | Enable the DSM:1 simulator CSC |
| dsm1.enabled | bool | `false` | Enable the DSM:1 CSC |
| dsm2-sim.enabled | bool | `false` | Enable the DSM:2 simulator CSC |
| dsm2.enabled | bool | `false` | Enable the DSM:2 CSC |
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
| m2-ess106-sim.enabled | bool | `false` | Enable the ESS:106 simulator CSC |
| m2-ess106.enabled | bool | `false` | Enable the ESS:106 CSC |
| mtdome-ess01-sim.enabled | bool | `false` | Enable the ESS:101 simulator CSC |
| mtdome-ess01.enabled | bool | `false` | Enable the ESS:101 CSC |
| mtdome-ess02-sim.enabled | bool | `false` | Enable the ESS:102 simulator CSC |
| mtdome-ess02.enabled | bool | `false` | Enable the ESS:102 CSC |
| mtdome-ess03-sim.enabled | bool | `false` | Enable the ESS:103 simulator CSC |
| mtdome-ess03.enabled | bool | `false` | Enable the ESS:103 CSC |
| tma-ess01-sim.enabled | bool | `false` | Enable the ESS:1 simulator CSC |
| tma-ess01.enabled | bool | `false` | Enable the ESS:1 CSC |
| tma-ess104-sim.enabled | bool | `false` | Enable the ESS:104 simulator CSC |
| tma-ess104.enabled | bool | `false` | Enable the ESS:104 CSC |
| tma-ess105-sim.enabled | bool | `false` | Enable the ESS:105 simulator CSC |
| tma-ess105.enabled | bool | `false` | Enable the ESS:105 CSC |
