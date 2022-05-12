# production-tools

A collection of utility pages for monitoring data processing.

**Homepage:** <https://github.com/lsst-sqre/production-tools>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the production-tools deployment pod |
| environment | object | `{}` |  |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the production-tools image |
| image.repository | string | `"lsstdm/production_tools"` | Image to use in the production-tools deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.gafaelfawrAuthQuery | string | `"scope=exec:portal"` | Gafaelfawr Auth Query string (default, unauthenticated) |
| ingress.pathType | string | `"Prefix"` | Path type for the ingress rule |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selection rules for the production-tools deployment pod |
| podAnnotations | object | `{}` | Annotations for the production-tools deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the production-tools deployment pod |
| tolerations | list | `[]` | Tolerations for the production-tools deployment pod |
