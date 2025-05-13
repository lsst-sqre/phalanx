# fspurger

Purge RSP directories according to policy

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for fspurger |
| config.dryRun | bool | `false` | Report only; do not purge |
| config.logging.addTimestamps | bool | `false` | Add timestamps to log lines |
| config.logging.log_level | string | `"info"` | Level at which to log |
| config.logging.profile | string | `"production"` | "production" (JSON logs) or "development" (human-friendly) |
| config.policyFile | string | `"/etc/purger/policy.yaml"` | File holding purge policy |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the fspurger image |
| image.repository | string | `"ghcr.io/lsst-sqre/scratchpurger"` | fspurger image to use |
| image.tag | string | The appVersion of the chart | Tag of fspurger image to use |
| nfs.path | string | `"/share1/scratch"` | Path (on server) for served /scratch |
| nfs.server | string | None, must be set for each environment | Hostname or IP address for NFS server |
| nodeSelector | object | `{}` | Node selector rules for fspurger |
| podAnnotations | object | `{}` | Annotations for the fspurger pod |
| policy.directories[0].intervals | object | see `values.yaml`, but in short, never remove: each | If any of these times are older than specified, remove the file.  Zero means "never remove". environment must set its own values. |
| policy.directories[0].path | string | `"/scratch"` |  |
| policy.directories[0].threshold | string | `"1GiB"` | Files this large or larger will be subject to the "large" interval set |
| resources | object | See `values.yaml` | Resource limits and requests for the filesystem purger |
| schedule.schedule | string | `"05 03 * * *"` | Crontab entry for when to run. |
| slackAlerts | bool | `false` | Whether to enable Slack alerts. If set to true, `slack_webhook` must be set in the corresponding fspurger Vault secret. |
| tolerations | list | `[]` | Tolerations for fspurger |
