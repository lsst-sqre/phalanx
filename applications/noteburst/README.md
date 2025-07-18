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
| config.metrics.application | string | `"noteburst"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.nubladoControllerPathPrefix | string | `"/nublado"` | URL path prefix for the Nublado JupyterLab Controller service |
| config.sentry.enabled | bool | `false` | Whether to enable sentry at all |
| config.sentry.tracesSampleRate | int | `0` | A number between 0 and 1, controlling the percentage chance a given transaction will be sent to Sentry. 0 represents 0% while 1 represents 100%. This has no effect on error reporting, only tracing. |
| config.worker.identities | list | `[]` | Science Platform user identities that workers can acquire. Each item is an object with username and uuid keys |
| config.worker.imageReference | string | `""` | Nublado image reference, applicable when imageSelector is "reference" |
| config.worker.imageSelector | string | `"recommended"` | Nublado image stream to select: "recommended", "weekly" or "reference" |
| config.worker.jobTimeout | int | `300` | The maximum allowed notebook execution time, in seconds. |
| config.worker.keepAlive | string | `"hourly"` | Worker keep alive mode: "normal", "fast", "hourly", "daily", "disabled" |
| config.worker.maxConcurrentJobs | int | `1` | Max number of concurrent notebook executions per worker |
| config.worker.tokenLifetime | string | `"2419200"` | Worker token lifetime, in seconds. |
| config.worker.tokenScopes | string | `"exec:notebook,read:image,read:tap,read:alertdb"` | Nublado2 worker account's token scopes as a comma-separated list. |
| config.worker.workerCount | int | `1` | Number of workers to run |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.environmentName | string | Set by Argo CD Application | Name of the Phalanx environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
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
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset data on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"8Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount | int | `1` | Number of API pods to run |
| resources | object | See `values.yaml` | Resource requests and limits for noteburst |
| resources.noteburst | object | `{"limits":{"cpu":"1","memory":"512Mi"},"requests":{"cpu":"2m","memory":"128Mi"}}` | Resource limits and requests for the noteburst FastAPI pods |
| resources.noteburstWorker | object | `{"limits":{"cpu":"1","memory":"4000Mi"},"requests":{"cpu":"2m","memory":"256Mi"}}` | Resource limits and requests for the noteburst arq worker FastAPI pods |
| service.port | int | `80` | Port of the service to create and map to the ingress |
| service.type | string | `"ClusterIP"` | Type of service to create |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
