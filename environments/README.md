# science-platform

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| alert-stream-broker.enabled | bool | `false` |  |
| argo-workflows.enabled | bool | `false` |  |
| butlerRepositoryIndex | string | None, must be set | Butler repository index to use for this environment |
| cachemachine.enabled | bool | `false` |  |
| cert-manager.enabled | bool | `false` |  |
| datalinker.enabled | bool | `false` |  |
| environment | string | None, must be set | Name of the environment |
| exposurelog.enabled | bool | `false` |  |
| fqdn | string | None, must be set | Fully-qualified domain name where the environment is running |
| gafaelfawr.enabled | bool | `false` |  |
| giftless.enabled | bool | `false` |  |
| hips.enabled | bool | `false` |  |
| ingress-nginx.enabled | bool | `false` |  |
| kubernetes-replicator.enabled | bool | `false` |  |
| linters.enabled | bool | `false` |  |
| livetap.enabled | bool | `false` |  |
| mobu.enabled | bool | `false` |  |
| moneypenny.enabled | bool | `false` |  |
| narrativelog.enabled | bool | `false` |  |
| noteburst.enabled | bool | `false` |  |
| nublado.enabled | bool | `false` |  |
| nublado2.enabled | bool | `false` |  |
| obsloctap.enabled | bool | `false` |  |
| onepasswordUuid | string | `"dg5afgiadsffeklfr6jykqymeu"` | UUID of the 1Password item in which to find Vault tokens |
| ook.enabled | bool | `false` |  |
| plot-navigator.enabled | bool | `false` |  |
| portal.enabled | bool | `false` |  |
| postgres.enabled | bool | `false` |  |
| production-tools.enabled | bool | `false` |  |
| repoURL | string | `"https://github.com/lsst-sqre/phalanx.git"` | URL of the repository for all applications |
| sasquatch.enabled | bool | `false` |  |
| semaphore.enabled | bool | `false` |  |
| sherlock.enabled | bool | `false` |  |
| sqlproxy-cross-project.enabled | bool | `false` |  |
| squarebot.enabled | bool | `false` |  |
| squareone.enabled | bool | `false` |  |
| squash-api.enabled | bool | `false` |  |
| ssotap.enabled | bool | `false` |  |
| strimzi-access-operator.enabled | bool | `false` |  |
| strimzi-registry-operator.enabled | bool | `false` |  |
| strimzi.enabled | bool | `false` |  |
| tap-schema.enabled | bool | `false` |  |
| tap.enabled | bool | `false` |  |
| targetRevision | string | `"main"` | Revision of repository to use for all applications |
| telegraf-ds.enabled | bool | `false` |  |
| telegraf.enabled | bool | `false` |  |
| times-square.enabled | bool | `false` |  |
| vault-secrets-operator.enabled | bool | `false` |  |
| vaultPathPrefix | string | None, must be set | Prefix for Vault secrets for this environment |
| vo-cutouts.enabled | bool | `false` |  |
