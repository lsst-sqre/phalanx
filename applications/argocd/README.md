# argo-cd

Kubernetes application manager

**Homepage:** <https://argoproj.github.io/cd/>

## Source Code

* <https://github.com/argoproj/argo-cd>
* <https://github.com/argoproj/argo-helm>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| argo-cd.configs.cm."resource.compareoptions" | string | `"ignoreAggregatedRoles: true\n"` | Configure resource comparison |
| argo-cd.configs.params."server.basehref" | string | `"/argo-cd"` | Base href for `index.html` when running under a reverse proxy |
| argo-cd.configs.params."server.insecure" | bool | `true` | Do not use TLS (this is terminated at the ingress) |
| argo-cd.configs.secret.createSecret | bool | `false` | Create the Argo CD secret (we manage this with Vault) |
| argo-cd.controller.metrics.applicationLabels.enabled | bool | `true` | Enable adding additional labels to `argocd_app_labels` metric |
| argo-cd.controller.metrics.applicationLabels.labels | list | `["name","instance"]` | Labels to add to `argocd_app_labels` metric |
| argo-cd.controller.metrics.enabled | bool | `true` | Enable controller metrics service |
| argo-cd.global.logging.format | string | `"json"` | Set the global logging format. Either: `text` or `json` |
| argo-cd.notifications.metrics.enabled | bool | `true` | Enable notifications metrics service |
| argo-cd.redis.metrics.enabled | bool | `true` | Enable Redis metrics service |
| argo-cd.repoServer.metrics.enabled | bool | `true` | Enable repo server metrics service |
| argo-cd.server.ingress.annotations | object | Rewrite requests to remove `/argo-cd/` prefix | Additional annotations to add to the Argo CD ingress |
| argo-cd.server.ingress.enabled | bool | `true` | Create an ingress for the Argo CD server |
| argo-cd.server.ingress.ingressClassName | string | `"nginx"` | Ingress class to use for Argo CD ingress |
| argo-cd.server.ingress.pathType | string | `"ImplementationSpecific"` | Type of path expression for Argo CD ingress |
| argo-cd.server.ingress.paths | list | `["/argo-cd(/|$)(.*)"]` | Paths to route to Argo CD |
| argo-cd.server.metrics.enabled | bool | `true` | Enable server metrics service |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |