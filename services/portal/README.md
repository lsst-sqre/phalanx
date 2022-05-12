# portal

Rubin Science Platform portal aspect

**Homepage:** <https://github.com/lsst/suit>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the Portal pod |
| config.cleanupInterval | string | `"36h"` | How long results should be retained before being deleted |
| config.debug | string | `"FALSE"` | Set to `TRUE` to enable service debugging |
| config.visualizeFitsSearchPath | string | `"/datasets"` | Search path for FITS files |
| config.volumes.configHostPath | string | Use an `emptyDir` | hostPath to mount as configuration.  Set either this of `configNfs`, not both. |
| config.volumes.configNfs | object | Use an `emptyDir` | NFS information for a configuration.  If set, must have keys for path and server, Set either this of `configHostPath`, not both. |
| config.volumes.workareaHostPath | string | Use an `emptyDir` | hostPath to mount as a shared work area.  Set either this or `workareaNfs`, not both. |
| config.volumes.workareaNfs | object | Use an `emptyDir` | NFS information for a shared work area.  If set, must have keys for path and server.  Set either this or `workareaHostPath`, not both. |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Portal image |
| image.repository | string | `"ipac/suit"` | Portal image to use |
| image.tag | string | The appVersion of the chart | Tag of Portal image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.gafaelfawrAuthQuery | string | `"scope=exec:portal&delegate_to=portal&delegate_scope=read:tap"` | Gafaelfawr auth query string |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the Portal pod |
| podAnnotations | object | `{}` | Annotations for the Portal pod |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Redis image |
| redis.image.repository | string | `"redis"` | Redis image to use |
| redis.image.tag | string | `"6.2.7"` | Redis image tag to use |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | `{"limits":{"memory":"20Mi"}}` | Resource limits and requests |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount | int | `1` | Number of pods to start |
| resources | object | `{"limits":{"cpu":2,"memory":"6Gi"}}` | Resource limits and requests. The Portal will use (by default) 93% of container RAM.  This is a smallish Portal; tweak it as you need to in instance definitions in Phalanx. |
| securityContext | object | `{}` | Security context for the Portal pod |
| tolerations | list | `[]` | Tolerations for the Portal pod |
