# filestore-backup

Tool to manage Google Filestore backups

## Source Code

* <https://github.com/lsst-sqre/rubin-google-filestore-tools>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the filestore-backup pods |
| config.backup.debug | bool | `false` | Turn on debugging mode |
| config.backup.schedule | string | fields are minute hour day-of-month month day-of-week | Backup schedule, in Unix cron job format |
| config.fileShare | string | `"share1"` | File Share name for filestore instance.  Always "share1" unless storage is on an Enterprise tier |
| config.instance | string | None, must be set | Filestore instance (e.g. "fshare-instance-dev") |
| config.purge.debug | bool | `false` | Turn on debugging mode |
| config.purge.keep | int | `6` | Number of backups to keep when purging |
| config.purge.schedule | string | fields are minute hour day-of-month month day-of-week | Purge schedule, in Unix cron job format: |
| config.zone | string | `"b"` | Zone for Filestore instance (e.g. "b" from "us-central1-b") |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.gcpProjectId | string | Set by Argo CD | GCP Project ID |
| global.gcpRegion | string | Set by Argo CD | GCP Region |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the filestore-backup image |
| image.repository | string | `"ghcr.io/lsst-sqre/rubin-google-filestore-tools"` | Filestore-Backup image to use |
| image.tag | string | The appVersion of the chart | Tag of filestore-backup image to use |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the filestore-backup pods |
| podAnnotations | object | `{}` | Annotations for the filestore-backup pods |
| resources | object | `{}` | Resource limits and requests for the filestore-backup pods |
| tolerations | list | `[]` | Tolerations for the filestore-backup pods |
