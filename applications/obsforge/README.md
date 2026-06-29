# obsforge

A metadata enrichment service for Rubin Observatory observations

## Source Code

* <https://github.com/lsst-sqre/obsforge>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the obsforge deployment pod |
| config.arqMode | string | `"production"` | Mode for the arq queue dependency |
| config.arqQueueName | string | `"arq:queue"` | Name of the arq queue used by ObsForge |
| config.butlerLabel | string | `"prompt"` | Butler repository label used by worker enrichment |
| config.butlerRepository | string | None, must be set | Prompt Butler repository path or URL for worker enrichment |
| config.databaseUrl | string | None, must be set | PostgreSQL DSN for ObsForge durable state |
| config.enrichmentMaxTries | int | `5` | Maximum arq attempts for an enrichment job |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.obscoreConfig | string | None, must be set | Path or URL to the lsst.dax.obscore prompt.yaml config |
| config.obscoreDatasetType | string | `"preliminary_visit_image"` | Dataset type selected from the ObsCore exporter config |
| config.pathPrefix | string | `"/obsforge"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| config.updateSchema | bool | `false` | Whether to run Alembic schema migrations on install/upgrade |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsforge image |
| image.repository | string | `"ghcr.io/lsst-sqre/obsforge"` | Image to use in the obsforge deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the obsforge deployment pod |
| podAnnotations | object | `{}` | Annotations for the obsforge deployment pod |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password |
| redis.config.secretName | string | `"obsforge"` | Name of secret containing Redis password |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage. Redis is arq transport state; keeping persistence enabled preserves queued and in-flight jobs across restarts. |
| redis.persistence.size | string | `"100Mi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `nil` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `nil` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the obsforge deployment pod |
| schemaUpdate.affinity | object | `{}` | Affinity rules for the schema update job |
| schemaUpdate.nodeSelector | object | `{}` | Node selection rules for the schema update job |
| schemaUpdate.podAnnotations | object | `{}` | Annotations for the schema update job pod |
| schemaUpdate.resources | object | See `values.yaml` | Resource limits and requests for the schema update job |
| schemaUpdate.tolerations | list | `[]` | Tolerations for the schema update job |
| tolerations | list | `[]` | Tolerations for the obsforge deployment pod |
| worker.affinity | object | `{}` | Affinity rules for the obsforge worker pods |
| worker.autoscaling.enabled | bool | `true` | Enable autoscaling of obsforge worker pods |
| worker.autoscaling.maxReplicas | int | `10` | Maximum number of obsforge worker pods |
| worker.autoscaling.minReplicas | int | `1` | Minimum number of obsforge worker pods |
| worker.autoscaling.targetCPUUtilizationPercentage | int | `75` | Target CPU utilization of obsforge worker pods |
| worker.nodeSelector | object | `{}` | Node selection rules for the obsforge worker pods |
| worker.podAnnotations | object | `{}` | Annotations for the obsforge worker pods |
| worker.replicaCount | int | `1` | Number of worker pods to start if autoscaling is disabled |
| worker.resources | object | See `values.yaml` | Resource limits and requests for the obsforge worker pods |
| worker.tolerations | list | `[]` | Tolerations for the obsforge worker pods |
