# square-events

Kafka topics and users for SQuaRE Events.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.name | string | `"sasquatch"` |  |
| topics.slackViewSubmission.retentionMs | int | `1800000` | Retention period, in milliseconds, for the Slack `view_submission` interaction topic. These events drive project creation in templatebot, so retaining them well beyond the other Squarebot topics keeps the payload of a failed creation available for debugging and replay. |
