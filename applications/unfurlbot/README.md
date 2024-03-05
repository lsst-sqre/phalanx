# unfurlbot

Squarebot backend that unfurls Jira issues.

## Source Code

* <https://github.com/lsst-sqre/unfurlbot>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the unfurlbot deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of unfurlbot deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of unfurlbot deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of unfurlbot deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of unfurlbot deployment pods |
| config.jiraProjects | string | `"ADMIN, CCB, CAP, COMCAM, COMT, DM, EPO, FRACAS, IAM, IHS, IT, ITRFC, LOVE, LASD, LIT, LOPS, LVV, M1M3V, OPSIM, PHOSIM, PST, PSV, PUB, RFC, RM, SAFE, SIM, SPP, SBTT, SE, TSAIV, TCT, SECMVERIF, TMDC, TPC, TSEIA, TAS, TELV, TSSAL, TSS, TSSPP, WMP, PREOPS, OBS, SITCOM, BLOCK\n"` | Names of Jira projects to unfurl (comma-separated) |
| config.logLevel | string | `"INFO"` | Logging level: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" |
| config.redisUrl | string | `"redis://unfurlbot-redis:6379/0"` | URL to the local redis instance |
| config.topics.slackAppMention | string | `"lsst.square-events.squarebot.slack.app.mention"` | Kafka topic name for the Slack `app_mention` events |
| config.topics.slackMessageChannels | string | `"lsst.square-events.squarebot.slack.message.channels"` | Kafka topic name for the Slack `message.channels` events (public channels) |
| config.topics.slackMessageGroups | string | `"lsst.square-events.squarebot.slack.message.groups"` | Kafka topic name for the Slack `message.groups` events (private channels) |
| config.topics.slackMessageIm | string | `"lsst.square-events.squarebot.slack.message.im"` | Kafka topic name for the Slack `message.im` events (direct message channels) |
| config.topics.slackMessageMpim | string | `"lsst.square-events.squarebot.slack.message.mpim"` | Kafka topic name for the Slack `message.mpim` events (multi-person direct messages) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the unfurlbot image |
| image.repository | string | `"ghcr.io/lsst-sqre/unfurlbot"` | Image to use in the unfurlbot deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the unfurlbot deployment pod |
| podAnnotations | object | `{}` | Annotations for the unfurlbot deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | `{}` | Resource limits and requests for the unfurlbot deployment pod |
| tolerations | list | `[]` | Tolerations for the unfurlbot deployment pod |
