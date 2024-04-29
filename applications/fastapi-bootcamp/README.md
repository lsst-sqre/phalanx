# fastapi-bootcamp

Phalanx FastAPI tutorial application

## Source Code

* <https://github.com/lsst-sqre/fastapi-bootcamp>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the fastapi-bootcamp deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of fastapi-bootcamp deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of fastapi-bootcamp deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of fastapi-bootcamp deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of fastapi-bootcamp deployment pods |
| config.logLevel | string | `"INFO"` | Log level: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" |
| config.loggingProfile | string | `"production"` | Logging profile: "production" or "development"  (Development does not use structured logging.) |
| config.pathPrefix | string | `"/fastapi-bootcamp"` | Prefix for fastapi-bootcamp's API routes. |
| config.slackAlerts | bool | `true` | Whether to send alerts and status to Slack. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the fastapi-bootcamp image |
| image.repository | string | `"ghcr.io/lsst-sqre/fastapi-bootcamp"` | Image to use in the fastapi-bootcamp deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the fastapi-bootcamp deployment pod |
| podAnnotations | object | `{}` | Annotations for the fastapi-bootcamp deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the fastapi-bootcamp deployment pod |
| tolerations | list | `[]` | Tolerations for the fastapi-bootcamp deployment pod |
