# portal

Rubin Science Platform Portal Aspect

## Source Code

* <https://github.com/lsst/suit>
* <https://github.com/Caltech-IPAC/firefly>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the Portal pod |
| config.cleanupInterval | string | `"36h"` | How long results should be retained before being deleted |
| config.debug | string | `"FALSE"` | Set to `TRUE` to enable service debugging |
| config.hipsUrl | string | `/api/hips/images/color_gri` in the local Science Platform | URL for default HiPS service |
| config.livetap | string | `""` | Endpoint under `/api/` for the live TAP service on the instance, if present |
| config.ssotap | string | `""` | Endpoint under `/api/` for the DP0.3 SSO TAP service on the instance, if present |
| config.visualizeFitsSearchPath | string | `"/datasets"` | Search path for FITS files |
| config.volumes.config | object | use an `emptyDir` | configuration directory accessible read-only to all Portal pods |
| config.volumes.privateWorkarea | object | use an `emptyDir` | private work area accessible read-write to a single Portal pod |
| config.volumes.sharedWorkarea | object | use an `emptyDir` (will not be shared; see documentation) | work area accessible read-write to all Portal pods |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Portal image |
| image.repository | string | `"ipac/suit"` | Portal image to use |
| image.tag | string | The appVersion of the chart | Tag of Portal image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the Portal pod |
| podAnnotations | object | `{}` | Annotations for the Portal pod |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.config.secretKey | string | `"ADMIN_PASSWORD"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"portal-secret"` | Name of secret containing Redis password (may require changing if fullnameOverride is set) |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.enabled | bool | `false` | Whether to persist Redis storage. Setting this to false will use `emptyDir` and reset all data on every restart. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount | int | `1` | Number of pods to start |
| resources | object | See `values.yaml` | Resource limits and requests. The Portal will use (by default) 93% of container RAM.  This is a smallish Portal; tweak it as you need to in instance definitions in Phalanx. |
| securityContext | object | See `values.yaml` | Security context for the Portal pod |
| tolerations | list | `[]` | Tolerations for the Portal pod |
