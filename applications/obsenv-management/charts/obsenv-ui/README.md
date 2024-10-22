# obsenv-ui

Helm chart for the Observatory Environment Management UI.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the obsenv-ui deployment pod |
| config.authGroup | string | `"test-group"` | The group used to authorize users to change the package versions |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/obsenv-ui"` | URL path prefix |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsenv-ui image |
| image.repository | string | `"rubincr.lsst.org/obsenv-ui"` | Image to use in the obsenv-ui deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the obsenv-ui deployment pod |
| podAnnotations | object | `{}` | Annotations for the obsenv-ui deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the obsenv-ui deployment pod |
| tolerations | list | `[]` | Tolerations for the obsenv-ui deployment pod |
