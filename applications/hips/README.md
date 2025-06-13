# hips

HiPS tile server backed by Google Cloud Storage

## Source Code

* <https://github.com/lsst-sqre/crawlspace>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the hips deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of hips deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of hips deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of hips deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of hips deployment pods |
| config.buckets | string | None, must be set | A mapping of bucket keys to GCS buckets. /api/hips/v2/<bucket-key> will serve files out of the corresponding GCS bucket. |
| config.defaultBucket | string | `nil` | The name (not the key) of bucket to serve from the v1 endpoint (/api/hips) |
| config.gcsProject | string | None, must be set | Google Cloud project in which the underlying storage is located |
| config.logLevel | string | `"INFO"` | Choose from the text form of Python logging levels |
| config.serviceAccount | string | None, must be set | The Google service account that has an IAM binding to the `hips` Kubernetes service account and has access to the storage bucket |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the hips image |
| image.repository | string | `"ghcr.io/lsst-sqre/crawlspace"` | Image to use in the hips deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress |
| nodeSelector | object | `{}` | Node selection rules for the hips deployment pod |
| podAnnotations | object | `{}` | Annotations for the hips deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the hips deployment pod |
| tolerations | list | `[]` | Tolerations for the hips deployment pod |
