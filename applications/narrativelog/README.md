# narrativelog

Narrative log service

## Source Code

* <https://github.com/lsst-ts/narrativelog>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the narrativelog pod |
| autoscaling | object | `{"enabled":false,"maxReplicas":100,"minReplicas":1,"targetCPUUtilizationPercentage":80,"targetMemoryUtilizationPercentage":80}` | Narrativelog autoscaling settings |
| autoscaling.enabled | bool | false | enable narrativelog autoscaling |
| autoscaling.maxReplicas | int | `100` | maximum number of narrativelog replicas |
| autoscaling.minReplicas | int | `1` | minimum number of narrativelog replicas |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization for narrativelog pod autoscale calculations |
| autoscaling.targetMemoryUtilizationPercentage | int | `80` | Target memory utilization for narrativelog pod autoscale calculations |
| config | object | `{"site_id":""}` | Application-specific configuration |
| config.site_id | string | `""` | Site ID; a non-empty string of up to 16 characters. This should be different for each non-sandbox deployment. Sandboxes should use `test`. |
| db.database | string | `"narrativelog"` | database name |
| db.host | string | `"postgres.postgres"` | database host |
| db.port | int | `5432` | database port |
| db.user | string | `"narrativelog"` | database user |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"Always"` | Pull policy for the narrativelog image |
| image.repository | string | `"ghcr.io/lsst-ts/narrativelog"` | narrativelog image to use |
| image.tag | string | The appVersion of the chart | Tag of exposure image to use |
| ingress.auth.enabled | bool | `false` | Whether to require Gafaelfawr authentication for access |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the narrativelog pod |
| podAnnotations | object | `{}` | Annotations for the narrativelog pod |
| podSecurityContext | object | `{}` | Security context for the narrativelog pod |
| replicaCount | int | `1` | Number of narrativelog replicas to run |
| resources | object | `{}` | Resource limits and requests for the narrativelog pod |
| securityContext | object | `{}` | Security context for the narrativelog deployment |
| tolerations | list | `[]` | Tolerations for the narrativelog pod |
