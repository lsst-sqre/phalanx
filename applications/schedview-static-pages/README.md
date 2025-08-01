# schedview-static-pages

Server for static pages from schedview

## Source Code

* <https://github.com/lsst/schedview>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the schedview-static-pages deployment pod |
| config.persistentVolumeClaims[0].name | string | `"sdf-data-rubin"` |  |
| config.persistentVolumeClaims[0].storageClassName | string | `"sdf-data-rubin"` |  |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the schedview-static-pages image |
| image.repository | string | `"nginxinc/nginx-unprivileged"` | Image to use in the schedview-static-pages deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the schedview-static-pages deployment pod |
| podAnnotations | object | `{}` | Annotations for the schedview-static-pages deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the schedview-static-pages deployment pod |
| tolerations | list | `[]` | Tolerations for the schedview-static-pages deployment pod |
