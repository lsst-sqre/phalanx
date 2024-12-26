# calsys

Deployment for the Calibration System CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| atmonochromator.enabled | bool | `false` | Enabled the ATMonochromator CSC |
| atwhitelight.enabled | bool | `false` | Enabled the ATWhitelight CSC |
| cbp.enabled | bool | `false` | Enable the CBP:0 CSC |
| electrometer101-sim.enabled | bool | `false` | Enable the Electrometer:11 simulator CSC |
| electrometer101.enabled | bool | `false` | Enable the Electrometer:101 CSC |
| electrometer102-sim.enabled | bool | `false` | Enable the Electrometer:102 simulator CSC |
| electrometer102.enabled | bool | `false` | Enable the Electrometer:102 CSC |
| electrometer201-sim.enabled | bool | `false` | Enable the Electrometer:201 simulator CSC |
| electrometer201.enabled | bool | `false` | Enable the Electrometer:201 CSC |
| gcheaderservice1.enabled | bool | `false` | Enable the GCHeaderService:1 CSC |
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
| ledprojector-sim.enabled | bool | `false` | Enabled the LedProjector:0 simulator CSC |
| ledprojector.enabled | bool | `false` | Enabled the LedProjector:0 CSC |
| linearstage101-sim.enabled | bool | `false` | Enable the LinearStage:101 simulator CSC |
| linearstage101.enabled | bool | `false` | Enable the LinearStage:101 CSC |
| linearstage102-sim.enabled | bool | `false` | Enable the LinearStage:102 simulator CSC |
| linearstage102.enabled | bool | `false` | Enable the LinearStage:102 CSC |
| linearstage103-sim.enabled | bool | `false` | Enable the LinearStage:103 simulator CSC |
| linearstage103.enabled | bool | `false` | Enable the LinearStage:103 CSC |
| linearstage104-sim.enabled | bool | `false` | Enable the LinearStage:104 simulator CSC |
| linearstage104.enabled | bool | `false` | Enable the LinearStage:104 CSC |
| simulation-gencam.enabled | bool | `false` | Enabled the GenericCamera:1 CSC |
| tunablelaser-sim.enabled | bool | `false` | Enabled the TunableLaser:0 simulator CSC |
| tunablelaser.enabled | bool | `false` | Enabled the TunableLaser:0 CSC |
