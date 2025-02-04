# simonyitel

Deployment for the Simonyi Survey Telescope CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| ccheaderservice.enabled | bool | `false` | Enable the CCHeaderService CSC |
| ccoods.enabled | bool | `false` | Enable the CCOODS CSC |
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
| lasertracker1-sim.enabled | bool | `false` | Enable the LaserTracker:1 simulator CSC |
| lasertracker1.enabled | bool | `false` | Enable the LaserTracker:1 CSC |
| mtaircompressor1-sim.enabled | bool | `false` | Enable the MTAirCompressor:1 simulator CSC |
| mtaircompressor1.enabled | bool | `false` | Enable the MTAirCompressor:1 CSC |
| mtaircompressor2-sim.enabled | bool | `false` | Enable the MTAirCompressor:2 simulator CSC |
| mtaircompressor2.enabled | bool | `false` | Enable the MTAirCompressor:2 CSC |
| mtcamhexapod-sim.enabled | bool | `false` | Enable the MTHexapod:1 simulator CSC |
| mtcamhexapod.enabled | bool | `false` | Enable the MTHexapod:1 CSC |
| mtdome-sim.enabled | bool | `false` | Enable the MTDome simulator CSC |
| mtdome.enabled | bool | `false` | Enable the MTDome CSC |
| mtheaderservice.enabled | bool | `false` | Enable the MTHeaderService CSC |
| mtm1m3-sim.enabled | bool | `false` | Enable the MTM1M3 simulator CSC |
| mtm1m3.enabled | bool | `false` | Enable the MTM1M3 hardware simulator CSC |
| mtm1m3ts-sim.enabled | bool | `false` | Enable the MTM1M3TS simulator CSC |
| mtm2-sim.enabled | bool | `false` | Enable the MTM2 simulator CSC |
| mtm2.enabled | bool | `false` | Enable the MTM2 CSC |
| mtm2hexapod-sim.enabled | bool | `false` | Enable the MTHexapod:2 simulator CSC |
| mtm2hexapod.enabled | bool | `false` | Enable the MTHexapod:2 CSC |
| mtmount-sim.enabled | bool | `false` | Enable the MTMount simulator CSC |
| mtmount.enabled | bool | `false` | Enable the MTMount CSC |
| mtoods.enabled | bool | `false` | Enable the MTOODS simulator CSC |
| mtrotator-sim.enabled | bool | `false` | Enable the MTRotator simulator CSC |
| mtrotator.enabled | bool | `false` | Enable the MTRotator CSC |
| mtvms-m1m3-sim.enabled | bool | `false` | Enable the MTVMS:1 simulator CSC |
