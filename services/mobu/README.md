# mobu

Generate system load by pretending to be a random scientist

**Homepage:** <https://github.com/lsst-sqre/mobu>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the mobu frontend pod |
| autostart | list | `[]` | Autostart specification. Must be a list of mobu flock specifications. Each flock listed will be automatically started when mobu is started. |
| cachemachineImagePolicy | string | `"available"` | Cachemachine image policy.  Must be one of `desired` or `available`.  Determines whether cachemachine reports the images it has or the ones it wants.  Should be `desired` in environments with image streaming enabled (e.g. IDF). |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the mobu image |
| image.repository | string | `"ghcr.io/lsst-sqre/mobu"` | mobu image to use |
| image.tag | string | The appVersion of the chart | Tag of mobu image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.gafaelfawrAuthQuery | string | `"scope=exec:admin"` | Gafaelfawr auth query string |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the mobu frontend pod |
| podAnnotations | object | `{}` | Annotations for the mobu frontend pod |
| resources | object | `{}` | Resource limits and requests for the mobu frontend pod |
| tolerations | list | `[]` | Tolerations for the mobu frontend pod |
