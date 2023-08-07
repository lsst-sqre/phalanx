# rubintv

Continuous integration testing

## Source Code

* <https://github.com/lsst-sqre/rubin-tv>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| frontend.config.debug | bool | `false` | If set to true, enable more verbose logging. |
| frontend.image.affinity | object | `{}` | Affinity rules for the rubintv frontend pod |
| frontend.image.nodeSelector | object | `{}` | Node selector rules for the rubintv frontend pod |
| frontend.image.podAnnotations | object | `{}` | Annotations for the rubintv frontend pod |
| frontend.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the rubintv image |
| frontend.image.repository | string | `"ghcr.io/lsst-sqre/rubintv"` | rubintv frontend image to use |
| frontend.image.resources | object | `{}` | Resource limits and requests for the rubintv frontend pod |
| frontend.image.tag | string | The appVersion of the chart | Tag of rubintv image to use |
| frontend.image.tolerations | list | `[]` | Tolerations for the rubintv frontend pod |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.pathPrefix | string | `"/rubintv"` | Prefix for rubintv's API routes. |
| nameOverride | string | `""` | Override the base name for resources |
| workers.config.debug | bool | `false` | If set to true, enable more verbose logging. |
| workers.config.pathPrefix | string | `"/"` | Prefix for the (internal) worker APU routes |
| workers.image.affinity | object | `{}` | Affinity rules for the rubintv worker pod |
| workers.image.nodeSelector | object | `{}` | Node selector rules for the rubintv worker pod |
| workers.image.podAnnotations | object | `{}` | Annotations for the rubintv worker pod |
| workers.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the rubintv worker image |
| workers.image.repository | string | `"docker.io/lsstts/rubintv-broadcaster"` | rubintv worker image to use |
| workers.image.resources | object | `{}` | Resource limits and requests for the rubintv worker pod |
| workers.image.tag | string | None, must be set per-deployment | Tag of rubintv worker image to use |
| workers.image.tolerations | list | `[]` | Tolerations for the rubintv worker pod |
