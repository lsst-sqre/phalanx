# templatebot

Create new projects

## Source Code

* <https://github.com/lsst-sqre/templatebot>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the templatebot deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/templatebot"` | URL path prefix |
| config.templateRepoUrl | string | `"https://github.com/lsst/templates"` | URL for the template repository |
| config.topics.slackAppMention | string | `"lsst.square-events.squarebot.slack.app.mention"` | Kafka topic name for the Slack `app_mention` events |
| config.topics.slackBlockActions | string | `"lsst.square-events.squarebot.slack.interaction.block-actions"` | Kafka topic for Slack `block_actions` interaction events |
| config.topics.slackMessageIm | string | `"lsst.square-events.squarebot.slack.message.im"` | Kafka topic name for the Slack `message.im` events (direct message channels) |
| config.topics.slackViewSubmission | string | `"lsst.square-events.squarebot.slack.interaction.view-submission"` | Kafka topic for Slack `view_submission` interaction events |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the templatebot image |
| image.repository | string | `"ghcr.io/lsst-sqre/templatebot"` | Image to use in the templatebot deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the templatebot deployment pod |
| podAnnotations | object | `{}` | Annotations for the templatebot deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the templatebot deployment pod |
| tolerations | list | `[]` | Tolerations for the templatebot deployment pod |
