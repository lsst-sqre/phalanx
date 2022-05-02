

# times-square

A parameterized notebook web viewer for the Rubin Science Platform.

See the embedded Helm sub-charts for additional configuration docs:

- [`times-square` (API)](charts/times-square)
- [`times-square-ui` (Next.js / React front-end)](charts/times-square-ui)

## Requirements

| Repository | Name | Version |
|------------|------|---------|
|  | times-square | 1.0.0 |
|  | times-square-ui | 1.0.0 |
| https://charts.bitnami.com/bitnami | redis | 16.8.9 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by times-square Argo CD Application | Base URL for the environment |
| global.host | string | Set by times-square Argo CD Application | Host name for ingress |
| global.vaultSecretsPathPrefix | string | Set by times-square Argo CD Application | Base path for Vault secrets |
| redis.auth.enabled | bool | `false` |  |
| redis.fullnameOverride | string | `"times-square-redis"` |  |
| times-square-ui.fullnameOverride | string | `"times-square-ui"` |  |
| times-square-ui.image.pullPolicy | string | `"IfNotPresent"` |  |
| times-square-ui.image.tag | string | `"tickets-DM-34030"` |  |
| times-square.config.redisUrl | string | Points to embedded Redis | Redis URL |
| times-square.fullnameOverride | string | `"times-square"` |  |
| times-square.image.pullPolicy | string | `"IfNotPresent"` |  |
| times-square.image.tag | string | `"tickets-DM-34030"` |  |
