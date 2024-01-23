# ingress-nginx

Ingress controller

**Homepage:** <https://kubernetes.github.io/ingress-nginx/>

## Source Code

* <https://github.com/kubernetes/ingress-nginx>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress-nginx.controller.allowSnippetAnnotations | bool | `true` | Allow Ingress resources to add NGINX configuration snippets. This is required by Gafaelfawr. |
| ingress-nginx.controller.config.compute-full-forwarded-for | string | `"true"` | Put the complete path in `X-Forwarded-For`, not just the last hop, so that the client IP will be exposed to Gafaelfawr |
| ingress-nginx.controller.config.proxy-body-size | string | `"100m"` | Maximum size of the client request body (needs to be large enough to allow table uploads) |
| ingress-nginx.controller.config.server-snippet | string | See `values.yaml` | Add additional per-server configuration used by Gafaelfawr to report errors from the authorization layer |
| ingress-nginx.controller.config.ssl-redirect | string | `"true"` | Redirect all non-SSL access to SSL |
| ingress-nginx.controller.config.use-forwarded-headers | string | `"true"` | Enable the `X-Forwarded-For` processing |
| ingress-nginx.controller.metrics.enabled | bool | `true` | Enable metrics reporting via Prometheus |
| ingress-nginx.controller.podLabels | object | See `values.yaml` | Add labels used by `NetworkPolicy` objects to restrict access to the ingress and thus ensure that auth subrequest handlers run |
| ingress-nginx.controller.service.externalTrafficPolicy | string | `"Local"` | Force traffic routing policy to Local so that the external IP in `X-Forwarded-For` will be correct |
| vaultCertificate.enabled | bool | `false` | Whether to store ingress TLS certificate via vault-secrets-operator. Typically the `squareone` application owns it instead in an RSP. |
