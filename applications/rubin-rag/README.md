# rubin-rag

RAG helpers for documentation searches

## Source Code

* <https://github.com/lsst-dm/rubin_rag>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the rubin-rag deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/rubin-rag"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the rubin-rag image |
| image.repository | string | `"ghcr.io/lsst-dm/rubin_rag"` | Image to use in the rubin-rag deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the rubin-rag deployment pod |
| podAnnotations | object | `{}` | Annotations for the rubin-rag deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the rubin-rag deployment pod |
| tolerations | list | `[]` | Tolerations for the rubin-rag deployment pod |
| weaviate.authentication.anonymous_access.enabled | bool | `true` |  |
| weaviate.containerSecurityContext.allowPrivilegeEscalation | bool | `false` |  |
| weaviate.containerSecurityContext.fsGroup | int | `1000` |  |
| weaviate.containerSecurityContext.fsGroupChangePolicy | string | `"OnRootMismatch"` |  |
| weaviate.containerSecurityContext.privileged | bool | `false` |  |
| weaviate.containerSecurityContext.readOnlyRootFilesystem | bool | `true` |  |
| weaviate.containerSecurityContext.runAsGroup | int | `1000` |  |
| weaviate.containerSecurityContext.runAsNonRoot | bool | `true` |  |
| weaviate.containerSecurityContext.runAsUser | int | `1000` |  |
| weaviate.env.AUTHENTICATION_APIKEY_ENABLED | string | `"true"` |  |
| weaviate.env.AUTHENTICATION_APIKEY_USERS | string | `"admin"` |  |
| weaviate.env.AUTHORIZATION_ADMINLIST_ENABLED | string | `"true"` |  |
| weaviate.env.AUTHORIZATION_ADMINLIST_USERS | string | `"admin"` |  |
| weaviate.envSecrets.AUTHENTICATION_APIKEY_ALLOWED_KEYS | string | `"rubin-rag"` |  |
| weaviate.initContainers.ensureFileOwnershipContainer.enabled | bool | `true` |  |
| weaviate.initContainers.sysctlInitContainer.enabled | bool | `false` |  |
| weaviate.modules.generative-openai.enabled | bool | `true` |  |
| weaviate.modules.text2vec-openai.enabled | bool | `true` |  |
| weaviate.resources.limits.cpu | string | `"500m"` |  |
| weaviate.resources.limits.ephemeral-storage | string | `"1Gi"` |  |
| weaviate.resources.limits.memory | string | `"300Mi"` |  |
| weaviate.resources.requests.cpu | string | `"300m"` |  |
| weaviate.resources.requests.ephemeral-storage | string | `"512M"` |  |
| weaviate.resources.requests.memory | string | `"150Mi"` |  |
| weaviate.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| weaviate.securityContext.fsGroup | int | `1000` |  |
| weaviate.securityContext.fsGroupChangePolicy | string | `"OnRootMismatch"` |  |
| weaviate.securityContext.privileged | bool | `false` |  |
| weaviate.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| weaviate.securityContext.runAsGroup | int | `1000` |  |
| weaviate.securityContext.runAsNonRoot | bool | `true` |  |
| weaviate.securityContext.runAsUser | int | `1000` |  |
