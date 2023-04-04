# argo-workflows

Kubernetes workflow engine

**Homepage:** <https://argoproj.github.io/argo-workflows>

## Source Code

* <https://github.com/argoproj/argo-workflows>
* <https://github.com/argoproj/argo-helm>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| argo-workflows.crds.keep | bool | `false` |  |
| argo-workflows.server.baseHref | string | `"/argo-workflows/"` |  |
| argo-workflows.server.extraArgs[0] | string | `"--auth-mode=server"` |  |
| argo-workflows.server.ingress.enabled | bool | `false` |  |
| argo-workflows.server.sso.clientId.key | string | `"client-id"` |  |
| argo-workflows.server.sso.clientId.name | string | `"argo-sso-secret"` |  |
| argo-workflows.server.sso.clientSecret.key | string | `"client-secret"` |  |
| argo-workflows.server.sso.clientSecret.name | string | `"argo-sso-secret"` |  |
| argo-workflows.server.sso.insecureSkipVerify | bool | `true` |  |
| argo-workflows.server.sso.issuer | string | `"https://data-dev.lsst.cloud/argo-cd/api/dex"` |  |
| argo-workflows.server.sso.rbac.enabled | bool | `true` |  |
| argo-workflows.server.sso.redirectUrl | string | `"https://data-dev.lsst.cloud/argo-workflows/oauth2/callback"` |  |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
