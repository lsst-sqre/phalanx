# science-platform

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| applications.alert-stream-broker | bool | `false` | Enable the alert-stream-broker application |
| applications.argo-workflows | bool | `false` | Enable the argo-workflows application |
| applications.argocd | bool | `true` | Enable the Argo CD application. This must be enabled for all environments and is present here only because it makes parsing easier |
| applications.auxtel | bool | `false` | Enable the auxtel control system application |
| applications.butler | bool | `false` | Enable the butler application |
| applications.calsys | bool | `false` | Enable the calsys control system application |
| applications.cert-manager | bool | `true` | Enable the cert-manager application, required unless the environment makes separate arrangements to inject a current TLS certificate |
| applications.control-system-test | bool | `false` | Enable the control-system-test application |
| applications.datalinker | bool | `false` | Eanble the datalinker application |
| applications.eas | bool | `false` | Enable the eas control system application |
| applications.exposurelog | bool | `false` | Enable the exposurelog application |
| applications.gafaelfawr | bool | `true` | Enable the Gafaelfawr application. This is required by Phalanx since most other applications use `GafaelfawrIngress` |
| applications.giftless | bool | `false` | Enable the giftless application |
| applications.hips | bool | `false` | Enable the HiPS application |
| applications.ingress-nginx | bool | `true` | Enable the ingress-nginx application. This is required for all environments, but is still configurable because currently USDF uses an unsupported configuration with ingress-nginx deployed in a different cluster. |
| applications.jira-data-proxy | bool | `false` | Enable the jira-data-proxy application |
| applications.kubernetes-replicator | bool | `false` | Enable the kubernetes-replicator application |
| applications.linters | bool | `false` | Enable the linters application |
| applications.livetap | bool | `false` | Enable the livetap application |
| applications.love | bool | `false` | Enable the love control system application |
| applications.mobu | bool | `false` | Enable the mobu application |
| applications.monitoring | bool | `false` | Enable the monitoring application |
| applications.narrativelog | bool | `false` | Enable the narrativelog application |
| applications.next-visit-fan-out | bool | `false` | Enable the next-visit-fan-out application |
| applications.noteburst | bool | `false` | Enable the noteburst application (required by times-square) |
| applications.nublado | bool | `false` | Enable the nublado application (v3 of the Notebook Aspect) |
| applications.obsloctap | bool | `false` | Enable the obsloctap application |
| applications.obssys | bool | `false` | Enable the obssys control system application |
| applications.onepassword-connect | bool | `false` | Enable the onepassword-connect application |
| applications.ook | bool | `false` | Enable the ook application |
| applications.plot-navigator | bool | `false` | Enable the plot-navigator application |
| applications.portal | bool | `false` | Enable the portal application |
| applications.postgres | bool | `false` | Enable the in-cluster PostgreSQL server. Use of this server is discouraged in favor of using infrastructure SQL, but will remain supported for use cases such as minikube test deployments. |
| applications.production-tools | bool | `false` | Enable the production-tools application |
| applications.prompt-proto-service-hsc | bool | `false` | Enable the prompt-proto-service-hsc application |
| applications.prompt-proto-service-latiss | bool | `false` | Enable the prompt-proto-service-latiss application |
| applications.prompt-proto-service-lsstcam | bool | `false` | Enable the prompt-proto-service-lsstcam application |
| applications.prompt-proto-service-lsstcomcam | bool | `false` | Enable the prompt-proto-service-lsstcomcam application |
| applications.rubintv | bool | `false` | Enable the rubintv application |
| applications.sasquatch | bool | `false` | Enable the sasquatch application |
| applications.schedview-prenight | bool | `false` | Enable the schedview-prenight application |
| applications.schedview-snapshot | bool | `false` | Enable the schedview-snapshot application |
| applications.semaphore | bool | `false` | Enable the semaphore application |
| applications.sherlock | bool | `false` | Enable the sherlock application |
| applications.siav2 | bool | `false` | Enable the siav2 application |
| applications.simonyitel | bool | `false` | Enable the simonyitel control system application |
| applications.sqlproxy-cross-project | bool | `false` | Enable the sqlproxy-cross-project application |
| applications.squarebot | bool | `false` | Enable the squarebot application |
| applications.squareone | bool | `false` | Enable the squareone application |
| applications.ssotap | bool | `false` | Enable the ssotap application |
| applications.strimzi | bool | `false` | Enable the strimzi application |
| applications.strimzi-access-operator | bool | `false` | Enable the strimzi-access-operator application |
| applications.tap | bool | `false` | Enable the tap application |
| applications.telegraf | bool | `false` | Enable the telegraf application |
| applications.telegraf-ds | bool | `false` | Enable the telegraf-ds application |
| applications.times-square | bool | `false` | Enable the times-square application |
| applications.uws | bool | `false` | Enable the uws application. This includes the dmocps control system application. |
| applications.vault-secrets-operator | bool | `true` | Enable the vault-secrets-operator application. This is required for all environments. |
| applications.vo-cutouts | bool | `false` | Enable the vo-cutouts application |
| butlerRepositoryIndex | string | None, must be set | Butler repository index to use for this environment |
| controlSystem | string | `nil` | Configuration particular to the control system If this section is used, it can have the following parameters: _appNamespace_ (Set the namespace for the control system components) _imageTag_ (The image tag to use for control system images) _siteTag_ (The tag that tells the control system component where it is running) _topicName_ (The Kafka identifier for control system topics) _kafkaBrokerAddress_ (The Kafka broker address) _kafkaTopicReplicationFactor_ (The Kafka topic replication factor) _schemaRegistryUrl_ (The Schema Registry URL) _s3EndpointUrl_ (The S3 URL for the environment specific LFA) |
| fqdn | string | None, must be set | Fully-qualified domain name where the environment is running |
| name | string | None, must be set | Name of the environment |
| repoUrl | string | `"https://github.com/lsst-sqre/phalanx.git"` | URL of the repository for all applications |
| targetRevision | string | `"main"` | Revision of repository to use for all applications |
| vaultPathPrefix | string | None, must be set | Prefix for Vault secrets for this environment |
| vaultUrl | string | `"https://vault.lsst.codes/"` | URL of Vault server for this environment |
