# plot-navigator

Panel-based plot viewer.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| environment | object | `{}` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.repository | string | `"lsstdm/pipetask-plot-navigator"` |  |
| image.tag | string | `""` |  |
| ingress.annotations | object | `{}` |  |
| ingress.gafaelfawrAuthQuery | string | `"scope=exec:portal&delegate_to=plotnavigator"` |  |
