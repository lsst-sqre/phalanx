# cachemachine

JupyterLab image prepuller

## Source Code

* <https://github.com/lsst-sqre/cachemachine>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the cachemachine frontend pod |
| autostart | object | `{}` | Autostart configuration. Each key is the name of a class of images to pull, and the value is the JSON specification for which and how many images to pull. |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the cachemachine image |
| image.repository | string | `"lsstsqre/cachemachine"` | cachemachine image to use |
| image.tag | string | The appVersion of the chart | Tag of cachemachine image to use |
| ingress.annotations | object | `{}` | Additional annotations to add for endpoints that are authenticated. |
| ingress.anonymousAnnotations | object | `{}` | Additional annotations to add for endpoints that allow anonymous access, such as `/*/available`. |
| ingress.gafaelfawrAuthQuery | string | `"scope=exec:admin"` | Gafaelfawr auth query string |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the cachemachine frontend pod |
| podAnnotations | object | `{}` | Annotations for the cachemachine frontend pod |
| resources | object | `{}` | Resource limits and requests for the cachemachine frontend pod |
| serviceAccount | object | `{"annotations":{},"name":""}` | Secret names to use for all Docker pulls |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.name | string | Name based on the fullname template | Name of the service account to use |
| tolerations | list | `[]` | Tolerations for the cachemachine frontend pod |
