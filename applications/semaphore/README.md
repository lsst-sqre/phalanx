# semaphore

Semaphore is the user notification and messaging service for the Rubin Science Platform.

## Source Code

* <https://github.com/lsst-sqre/semaphore>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| config.enable_github_app | string | `"False"` | Toggle to enable the GitHub App functionality |
| config.github_app_id | string | `""` | GitHub application ID |
| config.log_level | string | `"INFO"` |  |
| config.logger_name | string | `"semaphore"` | Logger name |
| config.name | string | `"semaphore"` | Name of the service, and path where the external API is hosted. |
| config.phalanx_env | string | `""` | Name of the Phalanx environment where the application is installed TODO can this be set by a global? |
| config.profile | string | `"production"` |  |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD Application | Base URL for the environment |
| global.host | string | Set by Argo CD Application | Host name for ingress |
| global.vaultSecretsPathPrefix | string | Set by Argo CD Application | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-sqre/semaphore"` | Semaphore image repository |
| image.tag | string | The appVersion of the chart | Tag of the image |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.enabled | bool | `true` | Enable ingress |
| ingress.path | string | `"/semaphore"` | URL path prefix where the Semaphore API is hosted |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for pods |
| replicaCount | int | `1` | Number of Semaphore pods to run |
| resources | object | `{}` |  |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `false` | Specifies whether a service account should be created. |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
