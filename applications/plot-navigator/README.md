# plot-navigator

Panel-based plot viewer

## Source Code

* <https://github.com/lsst-dm/pipetask-plot-navigator>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.persistentVolumeClaims | list | `[]` | PersistentVolumeClaims to create. |
| config.volume_mounts | list | `[]` | Mount points for additional volumes |
| config.volumes | list | `[]` | Additional volumes to attach |
| environment | object | `{}` | Environment variables (e.g. butler configuration/auth parms) for panel |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.repository | string | `"ghcr.io/lsst-dm/pipetask-plot-navigator"` | plot-navigator image to use |
| image.tag | string | `""` |  |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
