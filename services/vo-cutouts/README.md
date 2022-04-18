# vo-cutouts

Image cutout service complying with IVOA SODA

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the vo-cutouts frontend pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with CloudSQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.30.0"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | `""` | Instance connection name for a CloudSQL PostgreSQL instance |
| cloudsql.serviceAccount | string | None, must be set | The Google service account that has an IAM binding to the `vo-cutouts` Kubernetes service accounts and has the `cloudsql.client` role, access to the GCS bucket, and ability to sign URLs as itself |
| config.butlerRepository | string | None, must be set | Configuration for the Butler repository to use |
| config.databaseUrl | string | None, must be set | URL for the PostgreSQL database |
| config.gcsBucketUrl | string | None, must be set | URL for the GCS bucket into which to store cutouts (must start with `s3`) |
| config.lifetime | string | 2592000 (30 days) | Lifetime of job results in seconds (quote so that Helm doesn't turn it into a floating point number) |
| config.loglevel | string | `"INFO"` | Choose from the text form of Python logging levels |
| config.syncTimeout | int | 60 (1 minute) | Timeout for results from a sync cutout in seconds |
| config.timeout | int | 600 (10 minutes) | Timeout for a single cutout job in seconds |
| cutoutWorker.affinity | object | `{}` | Affinity rules for the cutout worker pod |
| cutoutWorker.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for cutout workers |
| cutoutWorker.image.repository | string | `"lsstsqre/vo-cutouts-worker"` | Stack image to use for cutouts |
| cutoutWorker.image.tag | string | The appVersion of the chart | Tag of vo-cutouts worker image to use |
| cutoutWorker.nodeSelector | object | `{}` | Node selection rules for the cutout worker pod |
| cutoutWorker.podAnnotations | object | `{}` | Annotations for the cutout worker pod |
| cutoutWorker.replicaCount | int | `2` | Number of cutout worker pods to start |
| cutoutWorker.resources | object | `{}` | Resource limits and requests for the cutout worker pod |
| cutoutWorker.tolerations | list | `[]` | Tolerations for the cutout worker pod |
| databaseWorker.affinity | object | `{}` | Affinity rules for the database worker pod |
| databaseWorker.nodeSelector | object | `{}` | Node selection rules for the database worker pod |
| databaseWorker.podAnnotations | object | `{}` | Annotations for the database worker pod |
| databaseWorker.replicaCount | int | `1` | Number of database worker pods to start |
| databaseWorker.resources | object | `{}` | Resource limits and requests for the database worker pod |
| databaseWorker.tolerations | list | `[]` | Tolerations for the database worker pod |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the vo-cutouts image |
| image.repository | string | `"lsstsqre/vo-cutouts"` | vo-cutouts image to use |
| image.tag | string | The appVersion of the chart | Tag of vo-cutouts image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.gafaelfawrAuthQuery | string | `"scope=read:image"` | Gafaelfawr auth query string |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the vo-cutouts frontend pod |
| podAnnotations | object | `{}` | Annotations for the vo-cutouts frontend pod |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Redis image |
| redis.image.repository | string | `"redis"` | Redis image to use |
| redis.image.tag | string | `"6.2.6"` | Redis image tag to use |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"100Mi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount | int | `1` | Number of web frontend pods to start |
| resources | object | `{}` | Resource limits and requests for the vo-cutouts frontend pod |
| tolerations | list | `[]` | Tolerations for the vo-cutouts frontend pod |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.5.0](https://github.com/norwoodj/helm-docs/releases/v1.5.0)
