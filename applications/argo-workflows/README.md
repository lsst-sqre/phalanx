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
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| ingress.annotations."nginx.ingress.kubernetes.io/use-regex" | string | `"true"` |  |
| ingress.scopes[0] | string | `"exec:admin"` |  |
