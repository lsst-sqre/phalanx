# unfurlbot

Squarebot backend that unfurls Jira issues.

## Source Code

* <https://github.com/lsst-sqre/unfurlbot>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the unfurlbot deployment pod |
| config.jiraProjects | string | See `values.yaml` | Names of Jira projects to unfurl (comma-separated) |
| config.jiraTimeout | string | `"60s"` | Jira request timeout. Use `m` and `s` for time intervals. |
| config.jiraUrl | string | `"https://rubinobs.atlassian.net/"` | Jira base URL |
| config.logLevel | string | `"INFO"` | Logging level: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" |
| config.redisUrl | string | `"redis://unfurlbot-redis:6379/0"` | URL to the local redis instance |
| config.slackDebounceTime | string | `"600"` | Time (second) before an unfurl can be made to the same channel/thread for a given token |
| config.slackTriggerMessageTtl | string | `"60"` | Time (seconds) after which a triggering Slack message is considered stale and ignored. |
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
| image.tag | string | The appVersion of the chart | Image tag to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the unfurlbot deployment pod |
| podAnnotations | object | `{}` | Annotations for the unfurlbot deployment pod |
| redis.resources | object | see `values.yaml` | Resource requests and limits for the redis pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the unfurlbot deployment pod |
| tolerations | list | `[]` | Tolerations for the unfurlbot deployment pod |
