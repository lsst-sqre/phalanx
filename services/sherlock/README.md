# sherlock

Application ingress status and metrics

## Source Code

* <https://github.com/lsst-sqre/sherlock>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the sherlock deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of sherlock deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of sherlock deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of sherlock deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of sherlock deployment pods |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the sherlock image |
| image.repository | string | `"lsstsqre/sherlock"` | Image to use in the sherlock deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| imagePullSecrets | list | `[]` | Secret names to use for all Docker pulls |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.gafaelfawrAuthQuery | string | `"scope=exec:admin"` | Gafaelfawr auth query string (default, unauthenticated) |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selection rules for the sherlock deployment pod |
| podAnnotations | object | `{}` | Annotations for the sherlock deployment pod |
| publishUrl | string | `""` | URL to push status to via HTTP PUTs. |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the sherlock deployment pod |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` | Tolerations for the sherlock deployment pod |
