# apdb-backups-gcp

Copies APDB Backups to Google Cloud.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| gcp-tsop.additionalVolumeMounts | list | `[]` | Kubernetes YAML configs for extra container volume(s). Any volumes required by other config options are automatically handled by the Helm chart. |
| gcp-tsop.affinity | object | `{}` | Affinity rules for the gcp-tsop Pod |
| gcp-tsop.gcp.projectId | string | `""` | GCP Project ID to run the agent |
| gcp-tsop.image.pullPolicy | string | `IfNotPresent` in prod, `Always` in dev.  Set to `IfNotPresent` for scale testing in dev. | Pull policy for the gcp-tsop image |
| gcp-tsop.image.repository | string | `"gcr.io/cloud-ingest/tsop-agent"` | Image to use in the gcp-tsop deployment |
| gcp-tsop.image.tag | string | `"public-image-v1"` | Overrides the image tag whose default is the chart appVersion. |
| gcp-tsop.nodeSelector | object | `{}` | Node selection rules for the gcp-tsop pod |
| gcp-tsop.resources | object | See `values.yaml` | Kubernetes resource requests and limits |
| gcp-tsop.s3.endpointURL | string | `"https://s3dfrgw.slac.stanford.edu"` | S3 Endpoint URL |
| gcp-tsop.s3.metadataDisabled | string | `"true"` |  |
| gcp-tsop.tolerations | list | `[]` | Tolerations for the gcp-tsop pod |
