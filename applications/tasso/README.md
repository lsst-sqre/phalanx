# tasso

Cutout labeling service

## Source Code

* <https://github.com/lsst-dm/tasso>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the tasso deployment pod |
| config.databaseSchema | string | `"tasso"` | database schema |
| config.databaseUrl | string | `""` | database connection url |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/tasso-api"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the tasso image |
| image.repository | string | `"ghcr.io/lsst-dm/tasso"` | Image to use in the tasso deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the tasso deployment pod |
| podAnnotations | object | `{}` | Annotations for the tasso deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the tasso deployment pod |
| s3.disableBucketValidation | int | `0` | Set this to disable validation of S3 bucket names, allowing Ceph multi-tenant colon-separated names to be used. |
| s3.endpointUrl | string | None, must be set | S3 endpoint containing `imageBucket` |
| s3.imageBucket | string | None, must be set | Bucket containing the incoming raw images |
| tolerations | list | `[]` | Tolerations for the tasso deployment pod |
