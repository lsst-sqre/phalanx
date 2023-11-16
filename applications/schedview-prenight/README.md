# schedview-prenight

Run the schedview pre-night briefing dashboard.

**Homepage:** <https://schedview.lsst.io/>

## Source Code

* <https://github.com/lsst/schedview>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the schedview-prenight deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of schedview-prenight deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of schedview-prenight deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of schedview-prenight deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of schedview-prenight deployment pods |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the schedview-prenight image |
| image.repository | string | `"ghcr.io/lsst/schedview"` | Image to use in the schedview-prenight deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the schedview-prenight deployment pod |
| podAnnotations | object | `{}` | Annotations for the schedview-prenight deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the schedview-prenight deployment pod |
| tolerations | list | `[]` | Tolerations for the schedview-prenight deployment pod |
