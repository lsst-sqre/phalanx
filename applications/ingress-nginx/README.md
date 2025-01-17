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
| ingress-nginx.controller.config.annotations-risk-level | string | `"Critical"` | Level of dangerous annotations allowed. Must be set to `Critical` to allow snippets. |
| ingress-nginx.controller.config.compute-full-forwarded-for | string | `"true"` | Put the complete path in `X-Forwarded-For`, not just the last hop, so that the client IP will be exposed to Gafaelfawr |
| ingress-nginx.controller.config.large-client-header-buffers | string | `"4 64k"` | Size and number of the buffers used to read HTTP headers from clients. Increase this from its default size in case clients send large cookies. |
| ingress-nginx.controller.config.proxy-body-size | string | `"100m"` | Maximum size of the client request body (needs to be large enough to allow table uploads) |
| ingress-nginx.controller.config.proxy-buffer-size | string | `"64k"` | Maximum size of the buffer used to read HTTP headers from the backend or auth subrequest handler. This needs to be larger than the default because Gafaelfawr reflects all of the user's cookies other than the Gafaelfawr one. |
| ingress-nginx.controller.config.server-snippet | string | See `values.yaml` | Add additional per-server configuration used by Gafaelfawr to report errors from the authorization layer |
| ingress-nginx.controller.config.ssl-redirect | string | `"true"` | Redirect all non-SSL access to SSL |
| ingress-nginx.controller.config.use-forwarded-headers | string | `"true"` | Enable the `X-Forwarded-For` processing |
| ingress-nginx.controller.metrics.enabled | bool | `true` | Enable metrics reporting via Prometheus |
| ingress-nginx.controller.podLabels | object | See `values.yaml` | Add labels used by `NetworkPolicy` objects to restrict access to the ingress and thus ensure that auth subrequest handlers run |
| ingress-nginx.controller.resources | object | See `values.yaml` | Resource requests and limits for ingress-nginx controller |
| ingress-nginx.controller.service.externalTrafficPolicy | string | `"Local"` | Force traffic routing policy to Local so that the external IP in `X-Forwarded-For` will be correct |
| vaultCertificate.enabled | bool | `false` | Whether to get the ingress TLS certificate from Vault instead of Let's Encrypt |
