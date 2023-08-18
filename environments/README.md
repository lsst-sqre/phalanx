# science-platform

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| applications.alert-stream-broker.enabled | bool | `false` | Enable the alert-stream-broker application |
| applications.argo-workflows.enabled | bool | `false` | Enable the argo-workflows application |
| applications.argocd.enabled | bool | `true` | Enable the Argo CD application. This must be enabled for all environments and is present here only because it makes parsing easier |
| applications.cachemachine.enabled | bool | `false` | Enable the cachemachine application (required by nublado2) |
| applications.cert-manager.enabled | bool | `true` | Enable the cert-manager application, required unless the environment makes separate arrangements to inject a current TLS certificate |
| applications.datalinker.enabled | bool | `false` | Eanble the datalinker application |
| applications.exposurelog.enabled | bool | `false` | Enable the exposurelog application |
| applications.gafaelfawr.enabled | bool | `true` | Enable the Gafaelfawr application. This is required by Phalanx since most other applications use `GafaelfawrIngress` |
| applications.giftless.enabled | bool | `false` | Enable the giftless application |
| applications.hips.enabled | bool | `false` | Enable the HiPS application |
| applications.ingress-nginx.enabled | bool | `true` | Enable the ingress-nginx application. This is required for all environments, but is still configurable because currently USDF uses an unsupported configuration with ingress-nginx deployed in a different cluster. |
| applications.kubernetes-replicator.enabled | bool | `false` | Enable the kubernetes-replicator application |
| applications.linters.enabled | bool | `false` | Enable the linters application |
| applications.livetap.enabled | bool | `false` | Enable the livetap application |
| applications.mobu.enabled | bool | `false` | Enable the mobu application |
| applications.moneypenny.enabled | bool | `false` | Enable the moneypenny application (required by nublado2) |
| applications.monitoring.enabled | bool | `false` | Enable the monitoring application |
| applications.narrativelog.enabled | bool | `false` | Enable the narrativelog application |
| applications.noteburst.enabled | bool | `false` | Enable the noteburst application (required by times-square) |
| applications.nublado.enabled | bool | `false` | Enable the nublado application (v3 of the Notebook Aspect) |
| applications.nublado2.enabled | bool | `false` | Enable the nublado2 application (v2 of the Notebook Aspect, now deprecated). This should not be used for new environments. |
| applications.obsloctap.enabled | bool | `false` | Enable the obsloctap application |
| applications.ook.enabled | bool | `false` | Enable the ook application |
| applications.plot-navigator.enabled | bool | `false` | Enable the plot-navigator application |
| applications.portal.enabled | bool | `false` | Enable the portal application |
| applications.postgres.enabled | bool | `false` | Enable the in-cluster PostgreSQL server. Use of this server is discouraged in favor of using infrastructure SQL, but will remain supported for use cases such as minikube test deployments. |
| applications.production-tools.enabled | bool | `false` | Enable the production-tools application |
| applications.sasquatch.enabled | bool | `false` | Enable the sasquatch application |
| applications.semaphore.enabled | bool | `false` | Enable the semaphore application |
| applications.sherlock.enabled | bool | `false` | Enable the sherlock application |
| applications.sqlproxy-cross-project.enabled | bool | `false` | Enable the sqlproxy-cross-project application |
| applications.squarebot.enabled | bool | `false` | Enable the squarebot application |
| applications.squareone.enabled | bool | `false` | Enable the squareone application |
| applications.squash-api.enabled | bool | `false` | Enable the squash-api application |
| applications.ssotap.enabled | bool | `false` | Enable the ssotap application |
| applications.strimzi-access-operator.enabled | bool | `false` | Enable the strimzi-access-operator application |
| applications.strimzi.enabled | bool | `false` | Enable the strimzi application |
| applications.tap-schema.enabled | bool | `false` | Enable the tap-schema application |
| applications.tap.enabled | bool | `false` | Enable the tap application |
| applications.telegraf-ds.enabled | bool | `false` | Enable the telegraf-ds application |
| applications.telegraf.enabled | bool | `false` | Enable the telegraf application |
| applications.times-square.enabled | bool | `false` | Enable the times-square application |
| applications.vault-secrets-operator.enabled | bool | `true` | Enable the vault-secrets-operator application. This is required for all environments. |
| applications.vo-cutouts.enabled | bool | `false` | Enable the vo-cutouts application |
| butlerRepositoryIndex | string | None, must be set | Butler repository index to use for this environment |
| fqdn | string | None, must be set | Fully-qualified domain name where the environment is running |
| name | string | None, must be set | Name of the environment |
| onepasswordUuid | string | `"dg5afgiadsffeklfr6jykqymeu"` | UUID of the 1Password item in which to find Vault tokens |
| repoUrl | string | `"https://github.com/lsst-sqre/phalanx.git"` | URL of the repository for all applications |
| targetRevision | string | `"main"` | Revision of repository to use for all applications |
| vaultPathPrefix | string | None, must be set | Prefix for Vault secrets for this environment |
| vaultUrl | string | None, must be set | URL of Vault server for this environment |
