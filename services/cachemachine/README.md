# cachemachine

Service to prepull Docker images for the Science Platform

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the cachemachine frontend pod |
| autostart | object | `{}` | Autostart configuration. Each key is the name of a class of images to pull, and the value is the JSON specification for which and how many images to pull. |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the cachemachine image |
| image.repository | string | `"lsstsqre/cachemachine"` | cachemachine image to use |
| image.tag | string | The appVersion of the chart | Tag of cachemachine image to use |
| imagePullSecrets | list | `[{"name":"cachemachine-secret"}]` | Secret names to use for all Docker pulls |
| ingress.annotations | object | `{}` | Additional annotations to add for endpoints that are authenticated. |
| ingress.anonymousAnnotations | object | `{}` | Additional annotations to add for endpoints that allow anonymous access, such as `/*/available`. |
| ingress.enabled | bool | `true` | Whether to create an ingress |
| ingress.gafaelfawrAuthQuery | string | `"scope=exec:admin"` | Gafaelfawr auth query string |
| ingress.host | string | None, must be set if the ingress is enabled | Hostname for the ingress |
| ingress.tls | list | `[]` | Configures TLS for the ingress if needed. If multiple ingresses share the same hostname, only one of them needs a TLS configuration. |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the cachemachine frontend pod |
| podAnnotations | object | `{}` | Annotations for the cachemachine frontend pod |
| resources | object | `{}` | Resource limits and requests for the cachemachine frontend pod |
| service.port | int | `80` | Port of the service to create and map to the ingress |
| service.type | string | `"ClusterIP"` | Type of service to create |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.name | string | Name based on the fullname template | Name of the service account to use |
| tolerations | list | `[]` | Tolerations for the cachemachine frontend pod |
| vaultSecretsPath | string | None, must be set | Path to the Vault secret containing the Docker credentials |
