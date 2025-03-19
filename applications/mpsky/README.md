# mpsky

Solar System Ephemerides

## Source Code

* <https://github.com/mjuric/mpsky>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the mpsky deployment pod |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the mpsky image |
| image.repository | string | `"nginxdemos/hello"` | Image to use in the mpsky deployment  repository: "ghcr.io/lsst-sqre/mpsky" |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the mpsky deployment pod |
| podAnnotations | object | `{}` | Annotations for the mpsky deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the mpsky deployment pod |
| tolerations | list | `[]` | Tolerations for the mpsky deployment pod |
