# schedview-snapshot

Dashboard for examination of scheduler snapshots

**Homepage:** <https://schedview.lsst.io/>

## Source Code

* <https://github.com/lsst/schedview>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the schedview-snapshot deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of schedview-snapshot deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of schedview-snapshot deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of schedview-snapshot deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of schedview-snapshot deployment pods |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the schedview-snapshot image |
| image.repository | string | `"ghcr.io/lsst/schedview"` | Image to use in the schedview-snapshot deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the schedview-snapshot deployment pod |
| podAnnotations | object | `{}` | Annotations for the schedview-snapshot deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the schedview-snapshot deployment pod |
| tolerations | list | `[]` | Tolerations for the schedview-snapshot deployment pod |
