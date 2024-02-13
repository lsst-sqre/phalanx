# checkerboard

Identity mapping service

## Source Code

* <https://github.com/lsst-sqre/checkerboard>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the checkerboard frontend pod |
| config | object | `{"logLevel":"INFO","profile":"production"}` | Configuration for checkerboard server |
| config.logLevel | string | `"INFO"` | Choose from the text form of Python logging levels |
| config.profile | string | `"production"` | application Safir profile ("production" or "development") |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the checkerboard image |
| image.repository | string | `"ghcr.io/lsst-sqre/checkerboard"` | Checkerboard image to use |
| image.tag | string | The appVersion of the chart | Tag of checkerboard image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.path | string | `"/checkerboard"` | Path prefix where checkerboard is hosted |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the checkerboard frontend pod |
| podAnnotations | object | `{}` | Annotations for the checkerboard frontend pod |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"checkerboard-secret"` | Name of secret containing Redis password (may require changing if fullnameOverride is set) |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"1Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| resources | object | `{}` | Resource limits and requests for the checkerboard frontend pod |
| tolerations | list | `[]` | Tolerations for the checkerboard frontend pod |
