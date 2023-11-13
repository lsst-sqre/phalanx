# siav2

Simple Image Access v2 service

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the siav2 deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of siav2 deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of siav2 deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of siav2 deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of siav2 deployment pods |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the siav2 image |
| image.repository | string | `"docker.io/cbanek/siav2"` | Image to use in the siav2 deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the siav2 deployment pod |
| obsCoreTable | string | `"ivoa.ObsCore"` | ObsCore table on the TAP service to query |
| podAnnotations | object | `{}` | Annotations for the siav2 deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the siav2 deployment pod |
| tapService | string | `"tap"` | Local TAP service endpoint to query |
| tolerations | list | `[]` | Tolerations for the siav2 deployment pod |
| uws.affinity | object | `{}` | Affinity rules for the UWS database pod |
| uws.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the UWS database image |
| uws.image.repository | string | `"library/postgres"` | UWS database image to use |
| uws.image.tag | string | `"16.0"` | Tag of UWS database image to use |
| uws.nodeSelector | object | `{}` | Node selection rules for the UWS database pod |
| uws.podAnnotations | object | `{}` | Annotations for the UWS databse pod |
| uws.resources | object | `{"limits":{"cpu":2,"memory":"4Gi"},"requests":{"cpu":0.25,"memory":"1Gi"}}` | Resource limits and requests for the UWS database pod |
| uws.tolerations | list | `[]` | Tolerations for the UWS database pod |
