# tap-schema

The TAP_SCHEMA database

## Source Code

* <https://github.com/lsst/sdm_schemas>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the MySQL pod |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the tap-schema image |
| image.repository | string | `"lsstsqre/tap-schema-mock"` | tap-schema image to use |
| image.tag | string | The appVersion of the chart | Tag of tap-schema image to use |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the MySQL pod |
| podAnnotations | object | `{}` | Annotations for the MySQL pod |
| resources | object | `{}` | Resource limits and requests for the MySQL pod |
| tolerations | list | `[]` | Tolerations for the MySQL pod |
