# obsloctap

Publish observing schedule

## Source Code

* <https://github.com/lsst-dm/obsloctap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.obsplanLimit | int | `1000` | limit for obsplan query |
| config.obsplanTimeSpan | int | `24` | time span, if a time is provided in the query how man hours to look back |
| config.persistentVolumeClaims | list | `[]` | PersistentVolumeClaims to create. |
| config.separateSecrets | bool | `true` | Whether to use the new secrets management scheme |
| config.volume_mounts | list | `[]` | Mount points for additional volumes |
| config.volumes | list | `[]` | Additional volumes to attach |
| environment | object | `{}` | Environment variables (e.g. butler configuration/auth parms) for panel |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsloctap image |
| image.repository | string | `"ghcr.io/lsst-dm/obsloctap"` | obsloctap image to use |
| image.tag | string | The appVersion of the chart | Tag of obsloctap image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
