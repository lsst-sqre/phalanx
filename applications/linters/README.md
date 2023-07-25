# linters

Linters running for operational reasons

## Source Code

* <https://github.com/lsst-sqre/ops-linters>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the linter pod |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the linter image |
| image.repository | string | `"ghcr.io/lsst-sqre/ops-linters"` | linter image to use |
| image.tag | string | The appVersion of the chart | Tag of linter image to use |
| linterSchedule | string | `"0 0 * * *"` | Cron schedule string for linter checking (in UTC) |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the linter pod |
| podAnnotations | object | `{}` | Annotations for the linter pod |
| replicaCount | int | `1` | Number of web frontend pods to start |
| resources | object | `{}` | Resource limits and requests for the linter pod |
| tolerations | list | `[]` | Tolerations for the linter pod |