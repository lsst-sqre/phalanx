# obsenv-api

Helm chart for the Observatory Environment Management API.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the obsenv-api deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/obsenv-api"` | URL path prefix |
| config.useFakeObsenvManager | bool | `false` | Use fake obsenv management system |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsenv-api image |
| image.repository | string | `"rubincr.lsst.org/obsenv-api"` | Image to use in the obsenv-api deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nfsMount.containerPath | string | `"/net/obs-env"` | Path to mount obs-env directory into container |
| nfsMount.server | string | `""` | Server where the data lives |
| nfsMount.serverPath | string | `"/obs-env"` | Path on the server where the data lives |
| nodeSelector | object | `{}` | Node selection rules for the obsenv-api deployment pod |
| podAnnotations | object | `{}` | Annotations for the obsenv-api deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the obsenv-api deployment pod |
| securityContext.group | int | `72089` | Group ID |
| securityContext.user | int | `72091` | User ID |
| tolerations | list | `[]` | Tolerations for the obsenv-api deployment pod |
