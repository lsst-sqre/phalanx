# filestore-backup

Tool to manage Google Filestore backups

## Source Code

* <https://github.com/lsst-sqre/rubin-google-filestore-tool>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the filestore-backup pods |
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
| tool.backup.debug | bool | `false` | Turn on debugging mode |
| tool.backup.schedule | string | `"0 10 * * *"` | Backup schedule |
| tool.fileShare | string | `"share1"` | File Share name for filestore instance.  Always "share1" unless storage is on an Enterprise tier |
| tool.instance | string | Must be overridden in environment-specific values file | Filestore instance (e.g. "fshare-instance-dev") |
| tool.purge.debug | bool | `false` | Turn on debugging mode |
| tool.purge.keep | int | `6` | Number of backups to keep when purging |
| tool.purge.schedule | string | `"45 10 * * *"` | purge schedule |
| tool.zone | string | Must be overridden in environment-specific values file | Zone for Filestore instance (e.g. "b" from "us-central1-b") |
