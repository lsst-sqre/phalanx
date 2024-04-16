# auxtel

Deployment for the Auxiliary Telescope CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
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
| atdome-sim.enabled | bool | `false` | Enable the ATDome simulator CSC |
| atdome.enabled | bool | `false` | Enable the ATDome CSC |
| athexapod-sim.enabled | bool | `false` | Enable the ATHexapod simulator CSC |
| athexapod.enabled | bool | `false` | Enable the ATHexapod CSC |
| atmcs-sim.enabled | bool | `false` | Enable the ATMCS simulator CSC |
| atmcs.enabled | bool | `false` | Enable the ATMCS CSC |
| atpneumatics-sim.enabled | bool | `false` | Enable the ATPneumatics simulator CSC |
| atpneumatics.enabled | bool | `false` | Enable the ATPneumatics CSC |
| atspectrograph-sim.enabled | bool | `false` | Enable the ATSpectograph simulator CSC |
| atspectrograph.enabled | bool | `false` | Enable the ATSpectrograph CSC |
| csc_shared.pullSecrets | list | `[]` | This section holds pull secret specifications. NOTE: The pull secret is expected to be part of the pull-secret key in Vault. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the pull secret) |
| hexapod-sim.enabled | bool | `false` | Enable the hexapod controller simulator |
| hexapod-sim.image | object | `{"pullPolicy":"Always","repository":"ts-dockerhub.lsst.org/hexapod_simulator","tag":"latest"}` | This section holds the configuration of the container image |
| hexapod-sim.image.pullPolicy | string | `"Always"` | The policy to apply when pulling an image for deployment |
| hexapod-sim.image.repository | string | `"ts-dockerhub.lsst.org/hexapod_simulator"` | The Docker registry name of the container image |
| hexapod-sim.image.tag | string | `"latest"` | The tag of the container image |
| hexapod-sim.namespace | string | `"auxtel"` | This is the namespace in which the hexapod controller simulator will be placed |
