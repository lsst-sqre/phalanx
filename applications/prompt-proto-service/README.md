# prompt-proto-service

A Helm chart for Kubernetes

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalVolumeMounts | list | `[]` |  |
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| containerConcurrency | int | `1` |  |
| fullnameOverride | string | `"prompt-proto-service"` | Override the full name for resources (includes the release name) |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"ghcr.io/lsst-dm/prompt-proto-service"` |  |
| image.tag | string | `""` |  |
| imageNotifications.imageTimeout | string | `"120"` |  |
| imagePullSecrets | list | `[]` |  |
| knative | object | `{"ephemeralStorageLimit":"20Gi","ephemeralStorageRequest":"8Gi","timeout":900}` | Knative settings |
| nameOverride | string | `""` | Override the base name for resources |
| namespace | string | `"prompt-proto-service"` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{"class":"kpa.autoscaling.knative.dev"}` | Annotations for the prompt processing service |
| s3.disableBucketValidation | string | `"0"` |  |
| tolerations | list | `[]` |  |
