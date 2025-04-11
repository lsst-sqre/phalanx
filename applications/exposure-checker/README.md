# exposure-checker

An interface for visually identifying artifacts in Rubin images.

## Source Code

* <https://github.com/lsst-sitcom/rubin_exp_checker>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.butler_collection | string | `nil` | Default collection in the butler |
| config.butler_repo | string | `nil` | Butler path or alias to use |
| config.db.db_name | string | `"expchecker"` | Name of database |
| config.db.hostname | string | `nil` | Database configuration |
| config.db.username | string | `"expchecker"` | Username for DB connection |
| config.persistentVolumeClaims | list | `[]` | PersistentVolumeClaims to create. |
| config.s3_endpoint_url | string | `nil` | Object store URL |
| config.s3_profile_name | string | `nil` | Profile to use for object store bucket. |
| config.separateSecrets | bool | `true` | Whether to use the new secrets management scheme |
| config.volume_mounts | list | `[]` | Mount points for additional volumes |
| config.volumes | list | `[]` | Additional volumes to attach |
| environment | object | `{}` | Environment variables |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.repository | string | `"ghcr.io/lsst-sitcom/rubin_exp_checker"` | rubin_exp_checker image to use |
| image.tag | string | The appVersion of the chart | Tag of rubin_exp_checker image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| resources | object | see `values.yaml` | Resource limits and requests for the nodejs pod |
