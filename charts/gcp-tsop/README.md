# gcp-tsop

Google Cloud Transfer Agent On Prem

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalVolumeMounts | list | `[]` | Kubernetes YAML configs for extra container volume(s). Any volumes required by other config options are automatically handled by the Helm chart. |
| affinity | object | `{}` | Affinity rules for the gcp-tsop Pod |
| gcp.projectId | string | `""` | GCP Project ID to run the agent |
| image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev.  Set to `IfNotPresent` for scale testing in dev. | Pull policy for the gcp-tsop image |
| image.repository | string | `"gcr.io/cloud-ingest/tsop-agent"` | Image to use in the gcp-tsop deployment |
| image.tag | string | `"latest"` | Overrides the image tag whose default is the chart appVersion. |
| nodeSelector | object | `{}` | Node selection rules for the Prompt Porcessing pod |
| resources | object | See `values.yaml` | Kubernetes resource requests and limits |
| s3.endpointURL | string | `""` | S3 Endpoint URL |
| s3.metadataDisabled | string | `"true"` |  |
| tolerations | list | `[]` | Tolerations for the gcp-tsop pod |
