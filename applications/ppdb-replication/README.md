# ppdb-replication

Replicates data from the APDB to the PPDB

## Source Code

* <https://github.com/lsst/dax_ppdb>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the ppdb-replication deployment pod |
| config.additionalS3ProfileName | string | `nil` | Additional S3 profile name |
| config.additionalS3ProfileUrl | string | `nil` | Additional S3 profile URL |
| config.apdbConfig | string | `nil` | APDB config file resource |
| config.apdbIndexUri | string | `nil` | APDB index URI |
| config.checkInterval | string | `nil` | Time to wait before checking for new chunks, if no chunk appears |
| config.disableBucketValidation | int | `1` | Disable bucket validation in LSST S3 tools |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.maxWaitTime | string | `nil` | Maximum time to wait before replicating a chunk after next chunk appears |
| config.minWaitTime | string | `nil` | Minimum time to wait before replicating a chunk after next chunk appears |
| config.monLogger | string | `"lsst.dax.ppdb.monitor"` | Name of logger for monitoring |
| config.monRules | string | `nil` | Comma-separated list of monitoring filter rules |
| config.pathPrefix | string | `"/ppdb-replication"` | URL path prefix |
| config.persistentVolumeClaims | list | `[]` | Persistent volume claims |
| config.ppdbConfig | string | `nil` | PPDB config file resource |
| config.s3EndpointUrl | string | `nil` | S3 endpoint URL |
| config.updateExisting | bool | `false` | Allow updates to already replicated data |
| config.volumeMounts | list | `[]` | Volume mounts |
| config.volumes | list | `[]` | Volumes specific to the environment |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the ppdb-replication image |
| image.repository | string | `"ghcr.io/lsst/ppdb-replication"` | Image to use in the ppdb-replication deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the ppdb-replication deployment pod |
| podAnnotations | object | `{}` | Annotations for the ppdb-replication deployment pod |
| replicaCount | int | `1` | Number of deployment pods to start |
| resources | object | see `values.yaml` | Resource limits and requests for the ppdb-replication deployment pod |
| tolerations | list | `[]` | Tolerations for the ppdb-replication deployment pod |
