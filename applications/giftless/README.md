# giftless

Git-LFS server with GCS S3 backend

## Source Code

* <https://github.com/datopian/giftless>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the giftless frontend pod |
| config | object | YAML will be used as-is.  cf https://giftless.datopian.com/en/latest/configuration.html | Configuration for giftless server |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the giftless image |
| image.repository | string | `"docker.io/datopian/giftless"` | Giftless image to use |
| image.tag | string | The appVersion of the chart | Tag of giftless image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.hostname | string | Must be overridden in environment-specific values file | FQDN of giftless ingress |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the giftless frontend pod |
| podAnnotations | object | `{}` | Annotations for the giftless frontend pod |
| resources | object | `{}` | Resource limits and requests for the giftless frontend pod |
| server.debug | bool | `false` | Turn on debugging mode |
| server.port | int | `5000` | Port for giftless server to listen on |
| server.processes | int | `2` | Number of processes for server |
| server.threads | int | `2` | Number of threads per process |
| tolerations | list | `[]` | Tolerations for the giftless frontend pod |
