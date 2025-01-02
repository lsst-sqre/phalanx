# envsys

Deployment for the Environmental Awareness Systems CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| auxtel-ess201-sim.enabled | bool | `false` | Enable the ESS:201 simulator CSC |
| auxtel-ess201.enabled | bool | `false` | Enable the ESS:201 CSC |
| auxtel-ess202-sim.enabled | bool | `false` | Enable the ESS:202 simulator CSC |
| auxtel-ess202.enabled | bool | `false` | Enable the ESS:202 CSC |
| auxtel-ess203-sim.enabled | bool | `false` | Enable the ESS:203 simulator CSC |
| auxtel-ess203.enabled | bool | `false` | Enable the ESS:203 CSC |
| auxtel-ess204-sim.enabled | bool | `false` | Enable the ESS:204 simulator CSC |
| auxtel-ess204.enabled | bool | `false` | Enable the ESS:204 CSC |
| calibhill-ess301-sim.enabled | bool | `false` | Enable the ESS:301 simulator CSC |
| calibhill-ess301.enabled | bool | `false` | Enable the ESS:301 CSC |
| camera-ess111-sim.enabled | bool | `false` | Enable the ESS:111 simulator CSC |
| camera-ess111.enabled | bool | `false` | Enable the ESS:111 CSC |
| cleanroom-ess109-sim.enabled | bool | `false` | Enable the ESS:109 simulator CSC |
| cleanroom-ess109.enabled | bool | `false` | Enable the ESS:109 CSC |
| dimm1-sim.enabled | bool | `false` | Enable the DIMM:1 simulator CSC |
| dimm1.enabled | bool | `false` | Enable the DIMM:1 CSC |
| dimm2-sim.enabled | bool | `false` | Enable the DIMM:2 simulator CSC |
| dimm2.enabled | bool | `false` | Enable the DIMM:2 CSC |
| dream-sim.enabled | bool | `false` | Enable the DREAM simulator CSC |
| dream.enabled | bool | `false` | Enable the DREAM CSC |
| dsm1-sim.enabled | bool | `false` | Enable the DSM:1 simulator CSC |
| dsm1.enabled | bool | `false` | Enable the DSM:1 CSC |
| dsm2-sim.enabled | bool | `false` | Enable the DSM:2 simulator CSC |
| dsm2.enabled | bool | `false` | Enable the DSM:2 CSC |
| earthquake-ess302.enabled | bool | `false` | Enable ESS:302 CSC |
| eas-sim.enabled | bool | `false` | Enable the EAS simulator CSC |
| eas.enabled | bool | `false` | Enable the EAS CSC |
| epm1-sim.enabled | bool | `false` | Enable the EPM:1 simulator CSC |
| epm1.enabled | bool | `false` | Enable the EPM:1 CSC |
| epm301.enabled | bool | `false` | Enable the EPM:301 CSC |
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
| hvac.enabled | bool | `false` | Enable the HVAC CSC |
| m1m3-ess113-sim.enabled | bool | `false` | Enable the ESS:113 simulator CSC |
| m1m3-ess113.enabled | bool | `false` | Enable the ESS:113 CSC |
| m2-ess106-sim.enabled | bool | `false` | Enable the ESS:106 simulator CSC |
| m2-ess106.enabled | bool | `false` | Enable the ESS:106 CSC |
| m2-ess112-sim.enabled | bool | `false` | Enable the ESS:112 simulator CSC |
| m2-ess112.enabled | bool | `false` | Enable the ESS:112 CSC |
| mtdome-ess107-sim.enabled | bool | `false` | Enable the ESS:107 simulator CSC |
| mtdome-ess107.enabled | bool | `false` | Enable the ESS:107 CSC |
| mtdome-ess108-sim.enabled | bool | `false` | Enable the ESS:108 simulator CSC |
| mtdome-ess108.enabled | bool | `false` | Enable the ESS:108 CSC |
| tma-ess001-sim.enabled | bool | `false` | Enable the ESS:1 simulator CSC |
| tma-ess001.enabled | bool | `false` | Enable the ESS:1 CSC |
| tma-ess104-sim.enabled | bool | `false` | Enable the ESS:104 simulator CSC |
| tma-ess104.enabled | bool | `false` | Enable the ESS:104 CSC |
| tma-ess105-sim.enabled | bool | `false` | Enable the ESS:105 simulator CSC |
| tma-ess105.enabled | bool | `false` | Enable the ESS:105 CSC |
| tma-ess110-sim.enabled | bool | `false` | Enable the ESS:110 simulator CSC |
| tma-ess110.enabled | bool | `false` | Enable the ESS:110 CSC |
| weatherforecast.enabled | bool | `false` | Enable the WeatherForecast CSC |
