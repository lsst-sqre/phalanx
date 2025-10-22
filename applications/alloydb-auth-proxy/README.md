# alloydb-auth-proxy

Proxy service for connecting to AlloyDB from USDF

## Source Code

* <https://github.com/lsst-sqre/alloydb-auth-proxy>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the alloydb-auth-proxy deployment pod |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the alloydb-auth-proxy image |
| image.repository | string | `"ghcr.io/lsst-sqre/alloydb-auth-proxy"` | Image to use in the alloydb-auth-proxy deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the alloydb-auth-proxy deployment pod |
| podAnnotations | object | `{}` | Annotations for the alloydb-auth-proxy deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the alloydb-auth-proxy deployment pod |
| tolerations | list | `[]` | Tolerations for the alloydb-auth-proxy deployment pod |
