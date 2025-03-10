# gai-helpers

RAG helpers for documentation searches

## Source Code

* <https://github.com/lsst-sqre/gai-helpers>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the gai-helpers deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/gai-helpers"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the gai-helpers image |
| image.repository | string | `"ghcr.io/gmegh/gai-helpers"` | Image to use in the gai-helpers deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the gai-helpers deployment pod |
| podAnnotations | object | `{}` | Annotations for the gai-helpers deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the gai-helpers deployment pod |
| tolerations | list | `[]` | Tolerations for the gai-helpers deployment pod |
| weaviate.authentication.anonymous_access.enabled | bool | `true` |  |
| weaviate.env.AUTHENTICATION_APIKEY_ENABLED | string | `"true"` |  |
| weaviate.env.AUTHENTICATION_APIKEY_USERS | string | `"admin"` |  |
| weaviate.env.AUTHORIZATION_ADMINLIST_ENABLED | string | `"true"` |  |
| weaviate.env.AUTHORIZATION_ADMINLIST_USERS | string | `"admin"` |  |
| weaviate.envSecrets.AUTHENTICATION_APIKEY_ALLOWED_KEYS | string | `"gai-helpers"` |  |
| weaviate.limits.cpu | string | `"500m"` |  |
| weaviate.limits.memory | string | `"300Mi"` |  |
| weaviate.requests.cpu | string | `"300m"` |  |
| weaviate.requests.memory | string | `"150Mi"` |  |
