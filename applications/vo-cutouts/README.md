# vo-cutouts

Image cutout service complying with IVOA SODA

## Source Code

* <https://github.com/lsst-sqre/vo-cutouts>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.gracePeriod | int | `60` | Grace period in seconds to wait for cutout worker jobs to finish |
| config.lifetime | string | `"30d"` | Lifetime of job results in Safir `parse_timedelta` format |
| config.loglevel | string | `"INFO"` | Choose from the text form of Python logging levels |
| config.pathPrefix | string | `"/api/cutout"` | URL path prefix for the cutout API |
| config.serviceAccount | string | None, must be set | Google service account with an IAM binding to the `vo-cutouts` Kubernetes service accounts and has access to write to the GCS bucket and ability to sign URLs as itself |
| config.slackAlerts | bool | `true` | Whether to send Slack alerts for unexpected failures |
| config.storageBucketUrl | string | None, must be set | URL for the GCS bucket for results (must start with `gs`) |
| config.syncTimeout | string | `"1m"` | Timeout for results from a sync cutout in Safir `parse_timedelta` format |
| config.timeout | int | 600 (10 minutes) | Timeout for a single cutout job in seconds |
| cutoutWorker.affinity | object | `{}` | Affinity rules for the cutout worker pod |
| cutoutWorker.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for cutout workers |
| cutoutWorker.image.repository | string | `"ghcr.io/lsst-sqre/vo-cutouts-worker"` | Stack image to use for cutouts |
| cutoutWorker.image.tag | string | The appVersion of the chart | Tag of vo-cutouts worker image to use |
| cutoutWorker.nodeSelector | object | `{}` | Node selection rules for the cutout worker pod |
| cutoutWorker.podAnnotations | object | `{}` | Annotations for the cutout worker pod |
| cutoutWorker.replicaCount | int | `2` | Number of cutout worker pods to start |
| cutoutWorker.resources | object | See `values.yaml` | Resource limits and requests for the cutout worker pod |
| cutoutWorker.tolerations | list | `[]` | Tolerations for the cutout worker pod |
| databaseWorker.affinity | object | `{}` | Affinity rules for the database worker pod |
| databaseWorker.nodeSelector | object | `{}` | Node selection rules for the database worker pod |
| databaseWorker.podAnnotations | object | `{}` | Annotations for the database worker pod |
| databaseWorker.replicaCount | int | `1` | Number of database worker pods to start |
| databaseWorker.resources | object | See `values.yaml` | Resource limits and requests for the database worker pod |
| databaseWorker.tolerations | list | `[]` | Tolerations for the database worker pod |
| frontend.affinity | object | `{}` | Affinity rules for the vo-cutouts frontend pod |
| frontend.nodeSelector | object | `{}` | Node selector rules for the vo-cutouts frontend pod |
| frontend.podAnnotations | object | `{}` | Annotations for the vo-cutouts frontend pod |
| frontend.replicaCount | int | `1` | Number of web frontend pods to start |
| frontend.resources | object | See `values.yaml` | Resource limits and requests for the vo-cutouts frontend pod |
| frontend.tolerations | list | `[]` | Tolerations for the vo-cutouts frontend pod |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.butlerServerRepositories | string | Set by Argo CD | Butler repositories accessible via Butler server |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the vo-cutouts image |
| image.repository | string | `"ghcr.io/lsst-sqre/vo-cutouts"` | vo-cutouts image to use for the frontend and database workers |
| image.tag | string | The appVersion of the chart | Tag of vo-cutouts image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"vo-cutouts"` | Name of secret containing Redis password |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"100Mi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `nil` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `nil` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
