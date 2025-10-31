# argo-cd

Kubernetes application manager

**Homepage:** <https://argoproj.github.io/cd/>

## Source Code

* <https://github.com/argoproj/argo-cd>
* <https://github.com/argoproj/argo-helm>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| argo-cd.applicationSet.resources | object | See `values.yaml` | Resource limits and requests for the applicationSet server |
| argo-cd.configs.cm."application.resourceTrackingMethod" | string | `"label"` | Keep label-based tracking for now until Nublado is updated. |
| argo-cd.configs.cm."resource.compareoptions" | string | `"ignoreAggregatedRoles: true\n"` | Configure resource comparison |
| argo-cd.configs.params."server.basehref" | string | `"/argo-cd"` | Base href for `index.html` when running under a reverse proxy |
| argo-cd.configs.params."server.insecure" | bool | `true` | Do not use TLS (this is terminated at the ingress) |
| argo-cd.configs.params."server.rootpath" | string | `"/argo-cd"` | Server root path when running under a reverse proxy |
| argo-cd.configs.secret.createSecret | bool | `false` | Create the Argo CD secret (we manage this with Vault) |
| argo-cd.configs.styles | string | `nil` | Add css to configure ArgoCD styling |
| argo-cd.controller.metrics.applicationLabels.enabled | bool | `true` | Enable adding additional labels to `argocd_app_labels` metric |
| argo-cd.controller.metrics.applicationLabels.labels | list | `["name","instance"]` | Labels to add to `argocd_app_labels` metric |
| argo-cd.controller.metrics.enabled | bool | `true` | Enable controller metrics service |
| argo-cd.controller.resources | object | See `values.yaml` | Resource limits and requests for the application controller pods |
| argo-cd.dex.resources | object | See `values.yaml` | Resource limits and requests for the Dex server |
| argo-cd.global.logging.format | string | `"json"` | Set the global logging format. Either: `text` or `json` |
| argo-cd.notifications.metrics.enabled | bool | `true` | Enable notifications metrics service |
| argo-cd.notifications.resources | object | See `values.yaml` | Resource limits and requests for the notifications controller |
| argo-cd.redis.metrics.enabled | bool | `true` | Enable Redis metrics service |
| argo-cd.redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis controller |
| argo-cd.repoServer.metrics.enabled | bool | `true` | Enable repo server metrics service |
| argo-cd.repoServer.resources | object | See `values.yaml` | Resource limits and requests for the repo server pods |
| argo-cd.server.ingress.annotations | object | Configure the `letsencrypt-dns` TLS cert cluster issuer | Annotations to add to the ingress |
| argo-cd.server.ingress.enabled | bool | `true` | Create an ingress for the Argo CD server |
| argo-cd.server.ingress.ingressClassName | string | `"nginx"` | Ingress class to use for Argo CD ingress |
| argo-cd.server.ingress.path | string | `"/argo-cd"` | Paths to route to Argo CD |
| argo-cd.server.ingress.tls | bool | `true` | Enable TLS management for this ingress. Disable this if TLS should not use a Let's Encrypt TLS certificate. |
| argo-cd.server.metrics.enabled | bool | `true` | Enable server metrics service |
| argo-cd.server.resources | object | See `values.yaml` | Resource limits and requests for the Argo CD server |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
