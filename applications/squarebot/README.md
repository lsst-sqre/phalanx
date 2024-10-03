# squarebot

Squarebot feeds events from services like Slack and GitHub into the SQuaRE Events Kafka message bus running on Roundtable. Backend apps like Templatebot and Unfurlbot can subscribe to these events and take domain-specific action.

**Homepage:** <https://squarebot.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/squarebot>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| config.logLevel | string | `"INFO"` | Logging level: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" |
| config.topics.slackAppMention | string | `"lsst.square-events.squarebot.slack.app.mention"` | Kafka topic name for the Slack `app_mention` events |
| config.topics.slackBlockActions | string | `"lsst.square-events.squarebot.slack.interaction.block-actions"` | Kafka topic for Slack `block_actions` interaction events |
| config.topics.slackMessageChannels | string | `"lsst.square-events.squarebot.slack.message.channels"` | Kafka topic name for the Slack `message.channels` events (public channels) |
| config.topics.slackMessageGroups | string | `"lsst.square-events.squarebot.slack.message.groups"` | Kafka topic name for the Slack `message.groups` events (private channels) |
| config.topics.slackMessageIm | string | `"lsst.square-events.squarebot.slack.message.im"` | Kafka topic name for the Slack `message.im` events (direct message channels) |
| config.topics.slackMessageMpim | string | `"lsst.square-events.squarebot.slack.message.mpim"` | Kafka topic name for the Slack `message.mpim` events (multi-person direct messages) |
| config.topics.slackViewSubmission | string | `"lsst.square-events.squarebot.slack.interaction.view-submission"` | Kafka topic for Slack `view_submission` interaction events |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-sqre/squarebot"` | Squarebot image repository |
| image.tag | string | The appVersion of the chart | Tag of the image |
| imagePullSecrets | list | `[]` | Secret names to use for all Docker pulls |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.path | string | `"/squarebot"` | Path prefix where Squarebot is hosted |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for API and worker pods |
| replicaCount | int | `1` | Number of API pods to run |
| resources | object | See `values.yaml` | Resource requests and limits for Squarebot |
| service.port | int | `80` | Port of the service to create and map to the ingress |
| service.type | string | `"ClusterIP"` | Type of service to create |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
