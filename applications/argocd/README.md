# argo-cd

Kubernetes application manager

**Homepage:** <https://argoproj.github.io/cd/>

## Source Code

* <https://github.com/argoproj/argo-cd>
* <https://github.com/argoproj/argo-helm>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| argo-cd.configs.secret.createSecret | bool | `false` | Create the Argo CD secret (we manage this with Vault) |
| argo-cd.controller.metrics.applicationLabels.enabled | bool | `true` | Enable adding additional labels to `argocd_app_labels` metric |
| argo-cd.controller.metrics.applicationLabels.labels | list | `["name","instance"]` | Labels to add to `argocd_app_labels` metric |
| argo-cd.controller.metrics.enabled | bool | `true` | Enable controller metrics service |
| argo-cd.global.logging.format | string | `"json"` | Set the global logging format. Either: `text` or `json` |
| argo-cd.notifications.metrics.enabled | bool | `true` | Enable notifications metrics service |
| argo-cd.redis.metrics.enabled | bool | `true` | Enable Redis metrics service |
| argo-cd.repoServer.metrics.enabled | bool | `true` | Enable repo server metrics service |
| argo-cd.server.config."helm.repositories" | string | See `values.yaml` | Additional Helm repositories to use |
| argo-cd.server.config."resource.compareoptions" | string | Ignore aggregated cluster roles | Comparison options for resources |
| argo-cd.server.extraArgs | list | `["--basehref=/argo-cd","--insecure=true"]` | Extra arguments to pass to the Argo CD server |
| argo-cd.server.ingress.annotations | object | Rewrite requests to remove `/argo-cd/` prefix | Additional annotations to add to the Argo CD ingress |
| argo-cd.server.ingress.enabled | bool | `true` | Create an ingress for the Argo CD server |
| argo-cd.server.ingress.ingressClassName | string | `"nginx"` | Ingress class to use for Argo CD ingress |
| argo-cd.server.ingress.pathType | string | `"ImplementationSpecific"` | Type of path expression for Argo CD ingress |
| argo-cd.server.ingress.paths | list | `["/argo-cd(/|$)(.*)"]` | Paths to route to Argo CD |
| argo-cd.server.metrics.enabled | bool | `true` | Enable server metrics service |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
