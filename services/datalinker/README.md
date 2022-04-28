# datalinker

A Helm chart for Kubernetes

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
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the datalinker image |
| image.repository | string | `"lsstsqre/datalinker"` | Image to use in the datalinker deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.gafaelfawrAuthQuery | string | `""` | Gafaelfawr auth query string (default, unauthenticated) |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selection rules for the datalinker deployment pod |
| podAnnotations | object | `{}` | Annotations for the datalinker deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the datalinker deployment pod |
| tolerations | list | `[]` | Tolerations for the datalinker deployment pod |
