# turborepo-cache

Turborepo remote cache

## Source Code

* <https://github.com/ducktors/turborepo-remote-cache>
* <https://github.com/lsst-sqre/turborepo-cache-proxy>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cache.affinity | object | `{}` | Affinity rules for the cache deployment pod |
| cache.config.googleServiceAccount | string | Do not create a Kubernetes ServiceAccount | Google Cloud service account email for GKE workload identity |
| cache.config.storagePath | string | `""` | Storage path for the cache |
| cache.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the cache image |
| cache.image.repository | string | `"ducktors/turborepo-remote-cache"` | Image to use in the cache deployment |
| cache.image.tag | string | The appVersion of the chart | Tag of cache image to use |
| cache.nodeSelector | object | `{}` | Node selection rules for the cache deployment pod |
| cache.podAnnotations | object | `{}` | Annotations for the cache deployment pod |
| cache.replicaCount | int | `1` | Number of cache deployment pods to start |
| cache.resources | object | See `values.yaml` | Resource limits and requests for the cache deployment pod |
| cache.tolerations | list | `[]` | Tolerations for the cache deployment pod |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| proxy.affinity | object | `{}` | Affinity rules for the proxy deployment pod |
| proxy.config.logLevel | string | `"INFO"` | Log level for the proxy application |
| proxy.config.logProfile | string | `"production"` | Logging profile (production for JSON, development for human-friendly) |
| proxy.config.name | string | `"turborepo-cache-proxy"` | Name of the proxy application |
| proxy.config.pathPrefix | string | `"/turborepo-cache"` | URL path prefix for the proxy application |
| proxy.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the proxy image |
| proxy.image.repository | string | `"ghcr.io/lsst-sqre/turborepo-cache-proxy"` | Image to use for the proxy deployment |
| proxy.image.tag | string | `"1.0.0"` | Tag of proxy image to use |
| proxy.nodeSelector | object | `{}` | Node selection rules for the proxy deployment pod |
| proxy.podAnnotations | object | `{}` | Annotations for the proxy deployment pod |
| proxy.replicaCount | int | `1` | Number of proxy deployment pods to start |
| proxy.resources | object | See `values.yaml` | Resource limits and requests for the proxy deployment pod |
| proxy.tolerations | list | `[]` | Tolerations for the proxy deployment pod |
