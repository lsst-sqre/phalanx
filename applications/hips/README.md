# hips

HiPS tile server backed by Google Cloud Storage

## Source Code

* <https://github.com/lsst-sqre/crawlspace>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the crawlspace deployment pod |
| config.buckets | string | None, must be set | A mapping of bucket keys to GCS buckets. /api/hips/v2/<bucket-key>/some/file will serve the file <objectPrefix>/some/file from the corresponding bucket. |
| config.cacheMaxAge | int | `3600` | Max age of resources in client caches (seconds) |
| config.defaultBucketKey | string | `nil` | The key of bucket in the 'buckets' dict to serve from the v1 endpoint (/api/hips) |
| config.gcsProject | string | None, must be set | Google Cloud project in which the underlying storage is located |
| config.logLevel | string | `"INFO"` | Choose from the text form of Python logging levels |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/api/hips/v2"` | URL path prefix (current API) |
| config.serviceAccount | string | None, must be set | The Google service account that has an IAM binding to the `hips` Kubernetes service account and has access to the storage bucket |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| config.v1PathPrefix | string | `"/api/hips"` | URL path prefix (legacy API) |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the hips image |
| image.repository | string | `"ghcr.io/lsst-sqre/crawlspace"` | Image to use in the crawlspace deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress |
| nodeSelector | object | `{}` | Node selection rules for the crawlspace deployment pod |
| podAnnotations | object | `{}` | Annotations for the crawlspace deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the crawlspace deployment pod |
| tolerations | list | Tolerate GKE amd64 and arm64 taints | Tolerations for the Repertoire pod |
