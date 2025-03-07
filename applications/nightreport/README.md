# nightreport

Night report log service

## Source Code

* <https://github.com/lsst-ts/ts_nightreport>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the nightreport pod |
| autoscaling | object | `{"enabled":false,"maxReplicas":100,"minReplicas":1,"targetCPUUtilizationPercentage":80,"targetMemoryUtilizationPercentage":80}` | Narrativelog autoscaling settings |
| autoscaling.enabled | bool | false | enable nightreport autoscaling |
| autoscaling.maxReplicas | int | `100` | maximum number of nightreport replicas |
| autoscaling.minReplicas | int | `1` | minimum number of nightreport replicas |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization for nightreport pod autoscale calculations |
| autoscaling.targetMemoryUtilizationPercentage | int | `80` | Target memory utilization for nightreport pod autoscale calculations |
| config | object | `{"site_id":""}` | Application-specific configuration |
| config.site_id | string | `""` | Site ID; a non-empty string of up to 16 characters. This should be different for each non-sandbox deployment. Sandboxes should use `test`. |
| db.database | string | `"nightreport"` | database name |
| db.host | string | `"postgres.postgres"` | database host |
| db.port | int | `5432` | database port |
| db.user | string | `"nightreport"` | database user |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the nightreport image |
| image.repository | string | `"lsstts/nightreport"` | nightreport image to use |
| image.tag | string | The appVersion of the chart | Tag of exposure image to use |
| ingress.auth.enabled | bool | `false` | Whether to require Gafaelfawr authentication for access |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the nightreport pod |
| podAnnotations | object | `{}` | Annotations for the nightreport pod |
| podSecurityContext | object | `{}` | Security context for the nightreport pod |
| replicaCount | int | `1` | Number of nightreport replicas to run |
| resources | object | `{}` | Resource limits and requests for the nightreport pod |
| securityContext | object | `{}` | Security context for the nightreport deployment |
| tolerations | list | `[]` | Tolerations for the nightreport pod |
