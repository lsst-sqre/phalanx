# ingress-nginx

Ingress controller

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://kubernetes.github.io/ingress-nginx | ingress-nginx | 4.3.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress-nginx.controller.config.compute-full-forwarded-for | string | `"true"` |  |
| ingress-nginx.controller.config.large-client-header-buffers | string | `"4 64k"` |  |
| ingress-nginx.controller.config.proxy-body-size | string | `"100m"` |  |
| ingress-nginx.controller.config.proxy-buffer-size | string | `"64k"` |  |
| ingress-nginx.controller.config.ssl-redirect | string | `"true"` |  |
| ingress-nginx.controller.config.use-forwarded-headers | string | `"true"` |  |
| ingress-nginx.controller.metrics.enabled | bool | `true` |  |
| ingress-nginx.controller.podLabels."gafaelfawr.lsst.io/ingress" | string | `"true"` |  |
| ingress-nginx.controller.podLabels."hub.jupyter.org/network-access-proxy-http" | string | `"true"` |  |
| ingress-nginx.controller.service.externalTrafficPolicy | string | `"Local"` |  |
| vaultCertificate.enabled | bool | `false` | Whether to store ingress TLS certificate via vault-secrets-operator.  Typically "squareone" owns it instead in an RSP. |
