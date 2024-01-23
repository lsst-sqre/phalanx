# jira-data-proxy

Jira API read-only proxy for Times Square users.

## Source Code

* <https://github.com/lsst-sqre/jira-data-proxy>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the jira-data-proxy deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of jira-data-proxy deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of jira-data-proxy deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of jira-data-proxy deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of jira-data-proxy deployment pods |
| config.jiraUrl | string | `"https://jira.lsstcorp.org/"` | Jira base URL |
| config.logLevel | string | `"info"` | Logging level |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the jira-data-proxy image |
| image.repository | string | `"ghcr.io/lsst-sqre/jira-data-proxy"` | Image to use in the jira-data-proxy deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.path | string | `"/jira-data-proxy"` | Path prefix where jira-data-proxy is served |
| nodeSelector | object | `{}` | Node selection rules for the jira-data-proxy deployment pod |
| podAnnotations | object | `{}` | Annotations for the jira-data-proxy deployment pod |
| replicaCount | int | `2` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the jira-data-proxy deployment pod |
| tolerations | list | `[]` | Tolerations for the jira-data-proxy deployment pod |
