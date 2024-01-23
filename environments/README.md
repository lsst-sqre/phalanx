# science-platform

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| applications.infrastructure | object | `{"argocd":true,"cert-manager":true,"gafaelfawr":true,"ingress-nginx":true,"mobu":false,"postgres":false,"strimzi":false,"strimzi-access-operator":false,"vault-secrets-operator":true}` | Project infrastructure |
| applications.infrastructure.argocd | bool | `true` | Enable the Argo CD application. This must be enabled for all environments and is present here only because it makes parsing easier |
| applications.infrastructure.cert-manager | bool | `true` | Enable the cert-manager application, required unless the environment makes separate arrangements to inject a current TLS certificate |
| applications.infrastructure.gafaelfawr | bool | `true` | Enable the Gafaelfawr application. This is required by Phalanx since most other applications use `GafaelfawrIngress` |
| applications.infrastructure.ingress-nginx | bool | `true` | Enable the ingress-nginx application. This is required for all environments, but is still configurable because currently USDF uses an unsupported configuration with ingress-nginx deployed in a different cluster. |
| applications.infrastructure.mobu | bool | `false` | Enable the mobu application |
| applications.infrastructure.postgres | bool | `false` | Enable the in-cluster PostgreSQL server. Use of this server is discouraged in favor of using infrastructure SQL, but will remain supported for use cases such as minikube test deployments. |
| applications.infrastructure.strimzi | bool | `false` | Enable the strimzi application |
| applications.infrastructure.strimzi-access-operator | bool | `false` | Enable the strimzi-access-operator application |
| applications.infrastructure.vault-secrets-operator | bool | `true` | Enable the vault-secrets-operator application. This is required for all environments. |
| applications.monitoring | object | `{"linters":false,"sasquatch":false,"sherlock":false,"telegraf":false,"telegraf-ds":false}` | Project monitoring |
| applications.monitoring.linters | bool | `false` | Enable the linters application |
| applications.monitoring.sasquatch | bool | `false` | Enable the sasquatch application |
| applications.monitoring.sherlock | bool | `false` | Enable the sherlock application |
| applications.monitoring.telegraf | bool | `false` | Enable the telegraf application |
| applications.monitoring.telegraf-ds | bool | `false` | Enable the telegraf-ds application |
| applications.prompt | object | `{"next-visit-fan-out":false,"prompt-proto-service-hsc":false,"prompt-proto-service-latiss":false,"prompt-proto-service-lsstcam":false,"prompt-proto-service-lsstcomcam":false}` | Project Prompt Processing |
| applications.prompt.next-visit-fan-out | bool | `false` | Enable the next-visit-fan-out application |
| applications.prompt.prompt-proto-service-hsc | bool | `false` | Enable the prompt-proto-service-hsc application |
| applications.prompt.prompt-proto-service-latiss | bool | `false` | Enable the prompt-proto-service-latiss application |
| applications.prompt.prompt-proto-service-lsstcam | bool | `false` | Enable the prompt-proto-service-lsstcam application |
| applications.prompt.prompt-proto-service-lsstcomcam | bool | `false` | Enable the prompt-proto-service-lsstcomcam application |
| applications.roundtable | object | `{"checkerboard":false,"giftless":false,"kubernetes-replicator":false,"monitoring":false,"onepassword-connect":false,"ook":false,"sqrbot-sr":false,"squarebot":false}` | Project roundtable |
| applications.roundtable.checkerboard | bool | `false` | Enable the checkerboard application |
| applications.roundtable.giftless | bool | `false` | Enable the giftless application |
| applications.roundtable.kubernetes-replicator | bool | `false` | Enable the kubernetes-replicator application |
| applications.roundtable.monitoring | bool | `false` | Enable the monitoring application |
| applications.roundtable.onepassword-connect | bool | `false` | Enable the onepassword-connect application |
| applications.roundtable.ook | bool | `false` | Enable the ook application |
| applications.roundtable.sqrbot-sr | bool | `false` | Enable the sqrbot-sr application |
| applications.roundtable.squarebot | bool | `false` | Enable the squarebot application |
| applications.rsp | object | `{"butler":false,"datalinker":false,"filestore-backup":false,"hips":false,"jira-data-proxy":false,"livetap":false,"noteburst":false,"nublado":false,"portal":false,"semaphore":false,"siav2":false,"sqlproxy-cross-project":false,"squareone":false,"ssotap":false,"tap":false,"times-square":false,"vo-cutouts":false}` | Project RSP (Rubin Science Platform) |
| applications.rsp.butler | bool | `false` | Enable the butler application |
| applications.rsp.datalinker | bool | `false` | Eanble the datalinker application |
| applications.rsp.filestore-backup | bool | `false` | Enable the filestore-backup application |
| applications.rsp.hips | bool | `false` | Enable the HiPS application |
| applications.rsp.jira-data-proxy | bool | `false` | Enable the jira-data-proxy application |
| applications.rsp.livetap | bool | `false` | Enable the livetap application |
| applications.rsp.noteburst | bool | `false` | Enable the noteburst application (required by times-square) |
| applications.rsp.nublado | bool | `false` | Enable the nublado application (v3 of the Notebook Aspect) |
| applications.rsp.portal | bool | `false` | Enable the portal application |
| applications.rsp.semaphore | bool | `false` | Enable the semaphore application |
| applications.rsp.siav2 | bool | `false` | Enable the siav2 application |
| applications.rsp.sqlproxy-cross-project | bool | `false` | Enable the sqlproxy-cross-project application |
| applications.rsp.squareone | bool | `false` | Enable the squareone application |
| applications.rsp.ssotap | bool | `false` | Enable the ssotap application |
| applications.rsp.tap | bool | `false` | Enable the tap application |
| applications.rsp.times-square | bool | `false` | Enable the times-square application |
| applications.rsp.vo-cutouts | bool | `false` | Enable the vo-cutouts application |
| applications.rubin | object | `{"alert-stream-broker":false,"exposurelog":false,"narrativelog":false,"obsloctap":false,"plot-navigator":false,"production-tools":false,"rubintv":false,"schedview-prenight":false,"schedview-snapshot":false}` | Project Rubin (Additional Rubin Services) |
| applications.rubin.alert-stream-broker | bool | `false` | Enable the alert-stream-broker application |
| applications.rubin.exposurelog | bool | `false` | Enable the exposurelog application |
| applications.rubin.narrativelog | bool | `false` | Enable the narrativelog application |
| applications.rubin.obsloctap | bool | `false` | Enable the obsloctap application |
| applications.rubin.plot-navigator | bool | `false` | Enable the plot-navigator application |
| applications.rubin.production-tools | bool | `false` | Enable the production-tools application |
| applications.rubin.rubintv | bool | `false` | Enable the rubintv application |
| applications.rubin.schedview-prenight | bool | `false` | Enable the schedview-prenight application |
| applications.rubin.schedview-snapshot | bool | `false` | Enable the schedview-snapshot application |
| applications.telescope | object | `{"argo-workflows":false,"auxtel":false,"calsys":false,"control-system-test":false,"eas":false,"love":false,"obssys":false,"simonyitel":false,"uws":false}` | Project telescope |
| applications.telescope.argo-workflows | bool | `false` | Enable the argo-workflows application |
| applications.telescope.auxtel | bool | `false` | Enable the auxtel control system application |
| applications.telescope.calsys | bool | `false` | Enable the calsys control system application |
| applications.telescope.control-system-test | bool | `false` | Enable the control-system-test application |
| applications.telescope.eas | bool | `false` | Enable the eas control system application |
| applications.telescope.love | bool | `false` | Enable the love control system application |
| applications.telescope.obssys | bool | `false` | Enable the obssys control system application |
| applications.telescope.simonyitel | bool | `false` | Enable the simonyitel control system application |
| applications.telescope.uws | bool | `false` | Enable the uws application. This includes the dmocps control system application. |
| butlerRepositoryIndex | string | None, must be set | Butler repository index URI to use for this environment, for services that connect directly to the Butler database. |
| butlerServerRepositories | object | None, must be set | Butler repositories that can be accessed via Butler server, as a dictionary from repository label to URI. |
| controlSystem.appNamespace | string | None, must be set | Application namespacce for the control system deployment |
| controlSystem.imageTag | string | None, must be set | Image tag for the control system deployment |
| controlSystem.kafkaBrokerAddress | string | `"sasquatch-kafka-brokers.sasquatch:9092"` | Kafka broker address for the control system deployment |
| controlSystem.kafkaTopicReplicationFactor | int | `3` | Kafka topic replication factor for control system topics |
| controlSystem.s3EndpointUrl | string | None, must be set: "" | S3 endpoint (LFA) for the control system deployment |
| controlSystem.schemaRegistryUrl | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Schema registry URL for the control system deployment |
| controlSystem.siteTag | string | None, must be set | Site tag for the control system deployment |
| controlSystem.topicName | string | `"sal"` | Topic name tag for the control system deployment |
| fqdn | string | None, must be set | Fully-qualified domain name where the environment is running |
| name | string | None, must be set | Name of the environment |
| repoUrl | string | `"https://github.com/lsst-sqre/phalanx.git"` | URL of the repository for all applications |
| targetRevision | string | `"main"` | Revision of repository to use for all applications |
| vaultPathPrefix | string | None, must be set | Prefix for Vault secrets for this environment |
| vaultUrl | string | `"https://vault.lsst.codes/"` | URL of Vault server for this environment |
