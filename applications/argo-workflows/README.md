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
| argo-workflows.server.extraArgs[0] | string | `"--auth-mode=server"` |  |
| argo-workflows.server.ingress.enabled | bool | `true` |  |
| argo-workflows.server.ingress.ingressClassName | string | `"nginx"` |  |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
