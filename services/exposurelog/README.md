![AppVersion: 0.9.2](https://img.shields.io/badge/AppVersion-0.9.2-informational?style=flat-square)

# exposurelog

Exposure log service

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| config.butler_uri_1 | string | `""` |  |
| config.butler_uri_2 | string | `""` |  |
| config.nfs_path_1 | string | `""` |  |
| config.nfs_path_2 | string | `""` |  |
| config.nfs_server_1 | string | `""` |  |
| config.nfs_server_2 | string | `""` |  |
| config.site_id | string | `""` |  |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"Always"` |  |
| image.repository | string | `"lsstsqre/exposurelog"` |  |
| image.tag | string | `""` |  |
| imagePullSecrets[0].name | string | `"pull-secret"` |  |
| ingress.enabled | bool | `false` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `8080` |  |
| service.type | string | `"ClusterIP"` |  |
| tolerations | list | `[]` |  |
