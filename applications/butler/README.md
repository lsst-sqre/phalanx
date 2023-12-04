# butler

Server for Butler data abstraction service

## Source Code

* <https://github.com/lsst/daf_butler>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the butler deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of butler deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of butler deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of butler deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of butler deployment pods |
| config.configUri | string | `""` | URI to the file specifying the DirectButler configuration to be used by the butler server |
| config.pathPrefix | string | `"/api/butler"` | The prefix of the path portion of the URL where the Butler service will be exposed.  For example, if the service should be exposed at `https://data.lsst.cloud/api/butler`, this should be set to `/api/butler` |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the butler image |
| image.repository | string | `"ghcr.io/lsst/daf_butler"` | Image to use in the butler deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the butler deployment pod |
| podAnnotations | object | `{}` | Annotations for the butler deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the butler deployment pod |
| tolerations | list | `[]` | Tolerations for the butler deployment pod |
