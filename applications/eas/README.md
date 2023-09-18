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
| calibhill-ess01-sim.enabled | bool | `false` | Enable the ESS:301 simulator CSC |
| calibhill-ess01.enabled | bool | `false` | Enable the ESS:301 CSC |
| csc_collector.secrets | list | `[]` | This section holds secret specifications. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the secret) _key_ (The key in the vault store where the secret resides) _type_ (OPTIONAL: The secret type. Defaults to Opaque.) |
| dimm1-sim.enabled | bool | `false` | Enable the DIMM:1 simulator CSC |
| dimm1.enabled | bool | `false` | Enable the DIMM:1 CSC |
| dimm2-sim.enabled | bool | `false` | Enable the DIMM:2 simulator CSC |
| dimm2.enabled | bool | `false` | Enable the DIMM:2 CSC |
| dsm1-sim.enabled | bool | `false` | Enable the DSM:1 simulator CSC |
| dsm1.enabled | bool | `false` | Enable the DSM:1 CSC |
| dsm2-sim.enabled | bool | `false` | Enable the DSM:2 simulator CSC |
| dsm2.enabled | bool | `false` | Enable the DSM:2 CSC |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.controlSystemAppNamespace | string | Set by ArgoCD | Application namespacce for the control system deployment |
| global.controlSystemImageTag | string | Set by ArgoCD | Image tag for the control system deployment |
| global.controlSystemKafkaBrokerAddress | string | Set by ArgoCD | Kafka broker address for the control system deployment |
| global.controlSystemS3EndpointUrl | string | Set by ArgoCD | S3 endpoint (LFA) for the control system deployment |
| global.controlSystemSchemaRegistryUrl | string | Set by ArgoCD | Schema registry URL for the control system deployment |
| global.controlSystemSiteTag | string | Set by ArgoCD | Site tag for the control system deployment |
| global.controlSystemTopicName | string | Set by ArgoCD | Topic name tag for the control system deployment |
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
