# noteburst

Noteburst is a notebook execution service for the Rubin Science Platform.

**Homepage:** <https://noteburst.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/noteburst>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| config.hubPathPrefix | string | `"/nb"` | URL path prefix for the JupyterHub service |
| config.logLevel | string | `"INFO"` | Logging level: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" |
| config.nubladoControllerPathPrefix | string | `"/nublado"` | URL path prefix for the Nublado JupyterLab Controller service |
| config.worker.identities | list | `[]` | Science Platform user identities that workers can acquire. Each item is an object with username and uuid keys |
| config.worker.imageReference | string | `""` | Nublado image reference, applicable when imageSelector is "reference" |
| config.worker.imageSelector | string | `"recommended"` | Nublado image stream to select: "recommended", "weekly" or "reference" |
| config.worker.jobTimeout | int | `300` | The default notebook execution timeout, in seconds. |
| config.worker.keepAlive | string | `"normal"` | Worker keep alive mode: "normal", "fast", "disabled" |
| config.worker.tokenLifetime | string | `"2419200"` | Worker token lifetime, in seconds. |
| config.worker.tokenScopes | string | `"exec:notebook,read:image,read:tap,read:alertdb"` | Nublado2 worker account's token scopes as a comma-separated list. |
| config.worker.workerCount | int | `1` | Number of workers to run |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-sqre/noteburst"` | Noteburst image repository |
| image.tag | string | The appVersion of the chart | Tag of the image |
| imagePullSecrets | list | `[]` | Secret names to use for all Docker pulls |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.path | string | `"/noteburst"` | Path prefix where noteburst is hosted |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for API and worker pods |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"8Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount | int | `1` | Number of API pods to run |
| resources | object | `{}` |  |
| service.port | int | `80` | Port of the service to create and map to the ingress |
| service.type | string | `"ClusterIP"` | Type of service to create |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
