# obsenv-management

Rubin Observatory Environment Management System

## Source Code

* <https://github.com/lsst-ts/obsenv-api>
* <https://github.com/lsst-ts/obsenv-ui>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| obsenv-api.affinity | object | `{}` | Affinity rules for the obsenv-api deployment pod |
| obsenv-api.config.logLevel | string | `"INFO"` | Logging level |
| obsenv-api.config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| obsenv-api.config.pathPrefix | string | `"/obsenv-api"` | URL path prefix |
| obsenv-api.config.useFakeObsenvManager | bool | `false` | Use fake obsenv management system |
| obsenv-api.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsenv-api image |
| obsenv-api.image.repository | string | `"rubincr.lsst.org/obsenv-api"` | Image to use in the obsenv-api deployment |
| obsenv-api.image.tag | string | The appVersion of the chart | Tag of image to use |
| obsenv-api.ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| obsenv-api.nfsMount.containerPath | string | `"/net/obs-env"` | Path to mount obs-env directory into container |
| obsenv-api.nfsMount.server | string | `""` | Server where the data lives |
| obsenv-api.nfsMount.serverPath | string | `"/obs-env"` | Path on the server where the data lives |
| obsenv-api.nodeSelector | object | `{}` | Node selection rules for the obsenv-api deployment pod |
| obsenv-api.podAnnotations | object | `{}` | Annotations for the obsenv-api deployment pod |
| obsenv-api.replicaCount | int | `1` | Number of web deployment pods to start |
| obsenv-api.resources | object | See `values.yaml` | Resource limits and requests for the obsenv-api deployment pod |
| obsenv-api.securityContext.group | int | `72089` | Group ID |
| obsenv-api.securityContext.user | int | `72091` | User ID |
| obsenv-api.tolerations | list | `[]` | Tolerations for the obsenv-api deployment pod |
| obsenv-ui.affinity | object | `{}` | Affinity rules for the obsenv-ui deployment pod |
| obsenv-ui.config.authGroup | string | `"test-group"` | The group used to authorize users to change the package versions |
| obsenv-ui.config.logLevel | string | `"INFO"` | Logging level |
| obsenv-ui.config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| obsenv-ui.config.pathPrefix | string | `"/obsenv-ui"` | URL path prefix |
| obsenv-ui.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsenv-ui image |
| obsenv-ui.image.repository | string | `"rubincr.lsst.org/obsenv-ui"` | Image to use in the obsenv-ui deployment |
| obsenv-ui.image.tag | string | The appVersion of the chart | Tag of image to use |
| obsenv-ui.ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| obsenv-ui.nodeSelector | object | `{}` | Node selection rules for the obsenv-ui deployment pod |
| obsenv-ui.podAnnotations | object | `{}` | Annotations for the obsenv-ui deployment pod |
| obsenv-ui.replicaCount | int | `1` | Number of web deployment pods to start |
| obsenv-ui.resources | object | See `values.yaml` | Resource limits and requests for the obsenv-ui deployment pod |
| obsenv-ui.tolerations | list | `[]` | Tolerations for the obsenv-ui deployment pod |
