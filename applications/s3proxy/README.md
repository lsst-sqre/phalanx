# s3proxy

Simple application to gateway S3 URLs to HTTPS

## Source Code

* <https://github.com/lsst-dm/s3proxy>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the s3proxy deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/s3proxy"` | URL path prefix |
| config.profiles | list | `[]` | Profiles using different endpoint URLs and credentials |
| config.s3EndpointUrl | string | `""` | Default S3 endpoint URL |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the s3proxy image |
| image.repository | string | `"ghcr.io/lsst-dm/s3proxy"` | Image to use in the s3proxy deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the s3proxy deployment pod |
| podAnnotations | object | `{}` | Annotations for the s3proxy deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the s3proxy deployment pod |
| tolerations | list | `[]` | Tolerations for the s3proxy deployment pod |
