# jira-stats

Simple Jira Stats such as reviews per team member

## Source Code

* <https://github.com/lsst-dm/jira_stats>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the jira-stats deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/jira-stats"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the jira-stats image |
| image.repository | string | `"ghcr.io/lsst-dm/jira_stats"` | Image to use in the jira-stats deployment |
| image.tag | string | `"tickets-dm-44297"` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the jira-stats deployment pod |
| podAnnotations | object | `{}` | Annotations for the jira-stats deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the jira-stats deployment pod |
| tolerations | list | `[]` | Tolerations for the jira-stats deployment pod |
