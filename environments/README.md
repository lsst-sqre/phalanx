# science-platform

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| applications.alert-stream-broker | bool | `false` | Enable the alert-stream-broker application |
| applications.argo-workflows | bool | `false` | Enable the argo-workflows application |
| applications.argocd | bool | `true` | Enable the Argo CD application. This must be enabled for all environments and is present here only because it makes parsing easier |
| applications.cachemachine | bool | `false` | Enable the cachemachine application (required by nublado2) |
| applications.cert-manager | bool | `true` | Enable the cert-manager application, required unless the environment makes separate arrangements to inject a current TLS certificate |
| applications.datalinker | bool | `false` | Eanble the datalinker application |
| applications.exposurelog | bool | `false` | Enable the exposurelog application |
| applications.gafaelfawr | bool | `true` | Enable the Gafaelfawr application. This is required by Phalanx since most other applications use `GafaelfawrIngress` |
| applications.giftless | bool | `false` | Enable the giftless application |
| applications.hips | bool | `false` | Enable the HiPS application |
| applications.ingress-nginx | bool | `true` | Enable the ingress-nginx application. This is required for all environments, but is still configurable because currently USDF uses an unsupported configuration with ingress-nginx deployed in a different cluster. |
| applications.kubernetes-replicator | bool | `false` | Enable the kubernetes-replicator application |
| applications.linters | bool | `false` | Enable the linters application |
| applications.livetap | bool | `false` | Enable the livetap application |
| applications.mobu | bool | `false` | Enable the mobu application |
| applications.moneypenny | bool | `false` | Enable the moneypenny application (required by nublado2) |
| applications.monitoring | bool | `false` | Enable the monitoring application |
| applications.narrativelog | bool | `false` | Enable the narrativelog application |
| applications.next-visit-fan-out | bool | `false` | Enable the next-visit-fan-out application |
| applications.noteburst | bool | `false` | Enable the noteburst application (required by times-square) |
| applications.nublado | bool | `false` | Enable the nublado application (v3 of the Notebook Aspect) |
| applications.nublado2 | bool | `false` | Enable the nublado2 application (v2 of the Notebook Aspect, now deprecated). This should not be used for new environments. |
| applications.obsloctap | bool | `false` | Enable the obsloctap application |
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
| applications.semaphore | bool | `false` | Enable the semaphore application |
| applications.sherlock | bool | `false` | Enable the sherlock application |
| applications.siav2 | bool | `false` | Enable the siav2 application |
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
| applications.vault-secrets-operator | bool | `true` | Enable the vault-secrets-operator application. This is required for all environments. |
| applications.vo-cutouts | bool | `false` | Enable the vo-cutouts application |
| butlerRepositoryIndex | string | None, must be set | Butler repository index to use for this environment |
| fqdn | string | None, must be set | Fully-qualified domain name where the environment is running |
| name | string | None, must be set | Name of the environment |
| repoUrl | string | `"https://github.com/lsst-sqre/phalanx.git"` | URL of the repository for all applications |
| targetRevision | string | `"main"` | Revision of repository to use for all applications |
| vaultPathPrefix | string | None, must be set | Prefix for Vault secrets for this environment |
| vaultUrl | string | `"https://vault.lsst.codes/"` | URL of Vault server for this environment |
