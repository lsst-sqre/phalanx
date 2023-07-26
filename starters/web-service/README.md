# <CHARTNAME>

Helm starter chart for a new RSP service.

**Homepage:** <https://github.com/lsst-sqre/<CHARTNAME>>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the <CHARTNAME> deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of <CHARTNAME> deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of <CHARTNAME> deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of <CHARTNAME> deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of <CHARTNAME> deployment pods |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the <CHARTNAME> image |
| image.repository | string | `"ghcr.io/lsst-sqre/<CHARTNAME>"` | Image to use in the <CHARTNAME> deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the <CHARTNAME> deployment pod |
| podAnnotations | object | `{}` | Annotations for the <CHARTNAME> deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the <CHARTNAME> deployment pod |
| tolerations | list | `[]` | Tolerations for the <CHARTNAME> deployment pod |
