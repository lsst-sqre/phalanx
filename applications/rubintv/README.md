# rubintv

Continuous integration testing

## Source Code

* <https://github.com/lsst-sqre/rubin-tv>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the rubintv frontend pod |
| config.debug | bool | `false` | If set to true, enable more verbose logging. |
| config.pathPrefix | string | `"/rubintv"` | Prefix for rubintv's API routes. |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the rubintv image |
| image.repository | string | `"ghcr.io/lsst-sqre/rubintv"` | rubintv image to use |
| image.tag | string | The appVersion of the chart | Tag of rubintv image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the rubintv frontend pod |
| podAnnotations | object | `{}` | Annotations for the rubintv frontend pod |
| resources | object | `{}` | Resource limits and requests for the rubintv frontend pod |
| tolerations | list | `[]` | Tolerations for the rubintv frontend pod |
