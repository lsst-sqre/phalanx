# science-platform

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| appOfAppsName | string | `"app-of-apps"` | Name of the parent Argo CD app-of-apps that manages all the applications enabled for this environment |
| applications.alert-stream-broker | bool | `false` | Enable the alert-stream-broker application |
| applications.argo-workflows | bool | `false` | Enable the argo-workflows application |
| applications.argocd | bool | `true` | Enable the Argo CD application. This must be enabled for all environments and is present here only because it makes parsing easier |
| applications.auxtel | bool | `false` | Enable the auxtel control system application |
| applications.butler | bool | `false` | Enable the butler application |
| applications.calsys | bool | `false` | Enable the calsys control system application |
| applications.cert-manager | bool | `true` | Enable the cert-manager application, required unless the environment makes separate arrangements to inject a current TLS certificate |
| applications.checkerboard | bool | `false` | Enable the checkerboard application |
| applications.cm-service | bool | `false` | Enable the cm-service application |
| applications.control-system-test | bool | `false` | Enable the control-system-test application |
| applications.datalinker | bool | `false` | Eanble the datalinker application |
| applications.envsys | bool | `false` | Enable the envsys control system application |
| applications.exposurelog | bool | `false` | Enable the exposurelog application |
| applications.fastapi-bootcamp | bool | `false` | Enable the fastapi-bootcamp application |
| applications.filestore-backup | bool | `false` | Enable the filestore-backup application |
| applications.flink | bool | `false` | Enable the flink application |
| applications.gafaelfawr | bool | `true` | Enable the Gafaelfawr application. This is required by Phalanx since most other applications use `GafaelfawrIngress` |
| applications.ghostwriter | bool | `false` | Enable the ghostwriter application |
| applications.giftless | bool | `false` | Enable the giftless application |
| applications.hips | bool | `false` | Enable the HiPS application |
| applications.ingress-nginx | bool | `true` | Enable the ingress-nginx application. This is required for all environments, but is still configurable because currently USDF uses an unsupported configuration with ingress-nginx deployed in a different cluster. |
| applications.jira-data-proxy | bool | `false` | Enable the jira-data-proxy application |
| applications.livetap | bool | `false` | Enable the livetap application |
| applications.love | bool | `false` | Enable the love control system application |
| applications.mobu | bool | `false` | Enable the mobu application |
| applications.monitoring | bool | `false` | Enable the monitoring application |
| applications.narrativelog | bool | `false` | Enable the narrativelog application |
| applications.next-visit-fan-out | bool | `false` | Enable the next-visit-fan-out application |
| applications.noteburst | bool | `false` | Enable the noteburst application (required by times-square) |
| applications.nublado | bool | `false` | Enable the nublado application (v3 of the Notebook Aspect) |
| applications.obsenv-management | bool | `false` | Enable the obsenv-management application |
| applications.obsloctap | bool | `false` | Enable the obsloctap application |
| applications.obssys | bool | `false` | Enable the obssys control system application |
| applications.onepassword-connect | bool | `false` | Enable the onepassword-connect application |
| applications.ook | bool | `false` | Enable the ook application |
| applications.plot-navigator | bool | `false` | Enable the plot-navigator application |
| applications.portal | bool | `false` | Enable the portal application |
| applications.postgres | bool | `false` | Enable the in-cluster PostgreSQL server. Use of this server is discouraged in favor of using infrastructure SQL, but will remain supported for use cases such as minikube test deployments. |
| applications.ppdb-replication | bool | `false` | Enable the ppdb-replication application |
| applications.production-tools | bool | `false` | Enable the production-tools application |
| applications.prompt-proto-service-hsc | bool | `false` | Enable the prompt-proto-service-hsc application |
| applications.prompt-proto-service-hsc-gpu | bool | `false` | Enable the prompt-proto-service-hsc-gpu application |
| applications.prompt-proto-service-latiss | bool | `false` | Enable the prompt-proto-service-latiss application |
| applications.prompt-proto-service-lsstcam | bool | `false` | Enable the prompt-proto-service-lsstcam application |
| applications.prompt-proto-service-lsstcomcam | bool | `false` | Enable the prompt-proto-service-lsstcomcam application |
| applications.prompt-proto-service-lsstcomcamsim | bool | `false` | Enable the prompt-proto-service-lsstcomcamsim application |
| applications.rubintv | bool | `false` | Enable the rubintv application |
| applications.rubintv-dev | bool | `false` | Enable the rubintv-dev application |
| applications.s3proxy | bool | `false` | Enable the s3proxy application |
| applications.sasquatch | bool | `false` | Enable the sasquatch application |
| applications.sasquatch-backpack | bool | `false` | Enable the sasquatch-backpack application |
| applications.schedview-snapshot | bool | `false` | Enable the schedview-snapshot application |
| applications.semaphore | bool | `false` | Enable the semaphore application |
| applications.sia | bool | `false` | Enable the sia over butler application |
| applications.simonyitel | bool | `false` | Enable the simonyitel control system application |
| applications.sqlproxy-cross-project | bool | `false` | Enable the sqlproxy-cross-project application |
| applications.sqrbot-sr | bool | `false` | Enable the sqrbot-sr application |
| applications.squarebot | bool | `false` | Enable the squarebot application |
| applications.squareone | bool | `false` | Enable the squareone application |
| applications.ssotap | bool | `false` | Enable the ssotap application |
| applications.strimzi | bool | `false` | Enable the strimzi application |
| applications.strimzi-access-operator | bool | `false` | Enable the strimzi-access-operator application |
| applications.tap | bool | `false` | Enable the tap application |
| applications.tasso | bool | `false` | Enable the tasso application |
| applications.telegraf | bool | `false` | Enable the telegraf application |
| applications.telegraf-ds | bool | `false` | Enable the telegraf-ds application |
| applications.templatebot | bool | `false` | Enable the templatebot application |
| applications.times-square | bool | `false` | Enable the times-square application |
| applications.unfurlbot | bool | `false` | Enable the unfurlbot application |
| applications.uws | bool | `false` | Enable the uws application. This includes the dmocps control system application. |
| applications.vault | bool | `false` | Enable the vault application. This is the actual vault storage and there should only be one production and one development instance globally. |
| applications.vault-secrets-operator | bool | `true` | Enable the vault-secrets-operator application. This is required for all environments. |
| applications.vo-cutouts | bool | `false` | Enable the vo-cutouts application |
| applications.wobbly | bool | `false` | Enable the wobbly application, required if the environment will be running any Safir-based UWS services |
| butlerServerRepositories | object | None, must be set | Butler repositories that can be accessed via Butler server, as a dictionary from repository label to URI. |
| controlSystem.appNamespace | string | None, must be set | Application namespacce for the control system deployment |
| controlSystem.imageTag | string | None, must be set | Image tag for the control system deployment |
| controlSystem.kafkaBrokerAddress | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka broker address for the control system deployment |
| controlSystem.kafkaTopicReplicationFactor | int | `3` | Kafka topic replication factor for control system topics |
| controlSystem.s3EndpointUrl | string | None, must be set: "" | S3 endpoint (LFA) for the control system deployment |
| controlSystem.schemaRegistryUrl | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Schema registry URL for the control system deployment |
| controlSystem.siteTag | string | None, must be set | Site tag for the control system deployment |
| controlSystem.topicName | string | `"sal"` | Topic name tag for the control system deployment |
| fqdn | string | None, must be set | Fully-qualified domain name where the environment is running |
| name | string | None, must be set | Name of the environment |
| namespaceLabels | object | `{}` | Add labels for application namespaces. |
| repoUrl | string | `"https://github.com/lsst-sqre/phalanx.git"` | URL of the repository for all applications |
| targetRevision | string | `"main"` | Revision of repository to use for all applications |
| vaultPathPrefix | string | None, must be set | Prefix for Vault secrets for this environment |
| vaultUrl | string | `"https://vault.lsst.cloud/"` | URL of Vault server for this environment |
