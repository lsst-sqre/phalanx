# giftless

Git-LFS server with GCS S3 backend, with Rubin-specific auth

## Source Code

* <https://github.com/datopian/giftless>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the giftless frontend pod |
| config | object | `{"bucketName":"","serviceAccountReadonly":"","serviceAccountReadwrite":"","storageProjectName":""}` | Configuration for giftless server |
| config.bucketName | string | Must be overridden in environment-specific values file | Bucket name for GCS LFS Object Storage bucket |
| config.serviceAccountReadonly | string | Must be overridden in environment-specific values file | Read-only service account name for GCS LFS Object Storage bucket |
| config.serviceAccountReadwrite | string | Must be overridden in environment-specific values file | Read-write service account name for GCS LFS Object Storage bucket |
| config.storageProjectName | string | Must be overridden in environment-specific values file | Project name for GCS LFS Object Storage bucket |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the giftless image |
| image.repository | string | `"ghcr.io/datopian/giftless"` | Giftless image to use |
| image.tag | string | The appVersion of the chart | Tag of giftless image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.hostname | object | Must be overridden in environment-specific values file | FQDNs of giftless ingresses |
| ingress.hostname.readonly | string | Must be overridden in environment-specific values file | FQDN for the read-only giftless ingress |
| ingress.hostname.readwrite | string | Must be overridden in environment-specific values file | FQDN for the read-write giftless ingress |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the giftless frontend pod |
| podAnnotations | object | `{}` | Annotations for the giftless frontend pod |
| resources | object | See `values.yaml` | Resource limits and requests for the giftless frontend pod |
| server.debug | bool | `false` | Turn on debugging mode |
| server.readonly.processes | int | `2` | Number of processes for readonly server |
| server.readonly.queue | int | `1024` | Socket listen queue depth |
| server.readonly.replicas | int | `1` | Number of replicas for readonly server |
| server.readonly.threads | int | `2` | Number of threads per readonly process |
| server.readwrite.processes | int | `2` | Number of processes for readwrite server |
| server.readwrite.queue | int | `1024` | Socket listen queue depth |
| server.readwrite.replicas | int | `1` | Number of replicas for readwrite server |
| server.readwrite.threads | int | `2` | Number of threads per readwrite process |
| tolerations | list | `[]` | Tolerations for the giftless frontend pod |
