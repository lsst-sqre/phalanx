# datalinker

IVOA datalink service for Rubin Science Platform

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the datalinker deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of datalinker deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of datalinker deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of datalinker deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of datalinker deployment pods |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.butlerRepositoryIndex | string | Set by Argo CD | URI to the Butler configuration of available repositories |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the datalinker image |
| image.repository | string | `"ghcr.io/lsst-sqre/datalinker"` | Image to use in the datalinker deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.className | string | `"nginx"` | Ingress class |
| ingress.enabled | bool | `true` | Create an ingress resource |
| ingress.gafaelfawrAuthQuery | string | `""` | Gafaelfawr auth query string (default, unauthenticated) |
| ingress.path | string | `"/api/datalink"` | URL path to dispatch to the datalinker deployment pod |
| ingress.pathType | string | `"ImplementationSpecific"` | Path type for the ingress rule |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selection rules for the datalinker deployment pod |
| podAnnotations | object | `{}` | Annotations for the datalinker deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the datalinker deployment pod |
| service.port | int | `8080` | Port of the service to create and map to the ingress |
| service.type | string | `"ClusterIP"` | Type of service to create |
| tolerations | list | `[]` | Tolerations for the datalinker deployment pod |
