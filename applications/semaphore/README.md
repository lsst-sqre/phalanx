# semaphore

User notification and messaging service for the Rubin Science Platform.

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
| config.enableGithubApp | bool | `false` | Toggle to enable the GitHub App functionality |
| config.githubAppId | string | `nil` | GitHub application ID |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/semaphore"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.environmentName | string | Set by Argo CD | Name of the Phalanx environment |
| global.host | string | Set by Argo CD Application | Host name for ingress |
| global.vaultSecretsPathPrefix | string | Set by Argo CD Application | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-sqre/semaphore"` | Semaphore image repository |
| image.tag | string | The appVersion of the chart | Tag of the image |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for pods |
| replicaCount | int | `1` | Number of Semaphore pods to run |
| resources | object | See `values.yaml` | Resource requests and limits for Semaphore |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `false` | Specifies whether a service account should be created. |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
