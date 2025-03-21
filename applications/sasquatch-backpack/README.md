# sasquatch-backpack

Collection of APIs that feed into Sasquatch

**Homepage:** <https://sasquatch-backpack.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/sasquatch-backpack>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the sasquatch-backpack deployment pod |
| config.backpackRedisUrl | string | `"redis://sasquatch-backpack-redis.sasquatch-backpack:6379/0"` | Backpack Redis URL |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/sasquatch-backpack"` | URL path prefix |
| config.sasquatchRestProxyUrl | string | `""` | Sasquatch REST Proxy URL |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the sasquatch-backpack image |
| image.repository | string | `"ghcr.io/lsst-sqre/sasquatch-backpack"` | Image to use in the sasquatch-backpack deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the sasquatch-backpack deployment pod |
| podAnnotations | object | `{}` | Annotations for the sasquatch-backpack deployment pod |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage.  Setting this to false will use `emptyDir` which is not recommend in a production environment. |
| redis.persistence.size | string | `"1Gi"` | Amount of persistent storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| resources | object | See `values.yaml` | Resource limits and requests for the sasquatch-backpack deployment pod |
| schedule | string | `"0 0 * * *"` |  |
| tolerations | list | `[]` | Tolerations for the sasquatch-backpack deployment pod |
