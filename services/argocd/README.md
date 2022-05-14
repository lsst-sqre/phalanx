# argo-cd

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://argoproj.github.io/argo-helm | argo-cd | 4.5.12 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| argo-cd.configs.secret.createSecret | bool | `false` |  |
| argo-cd.controller.metrics.applicationLabels.enabled | bool | `true` |  |
| argo-cd.controller.metrics.applicationLabels.labels[0] | string | `"name"` |  |
| argo-cd.controller.metrics.applicationLabels.labels[1] | string | `"instance"` |  |
| argo-cd.controller.metrics.enabled | bool | `true` |  |
| argo-cd.notifications.metrics.enabled | bool | `true` |  |
| argo-cd.redis.enabled | bool | `true` |  |
| argo-cd.redis.metrics.enabled | bool | `true` |  |
| argo-cd.repoServer.metrics.enabled | bool | `true` |  |
| argo-cd.server.config."helm.repositories" | string | `"- url: https://lsst-sqre.github.io/charts/\n  name: lsst-sqre\n- url: https://ricoberger.github.io/helm-charts/\n  name: ricoberger\n- url: https://kubernetes.github.io/ingress-nginx/\n  name: ingress-nginx\n- url: https://charts.helm.sh/stable\n  name: stable\n- url: https://strimzi.io/charts/\n  name: strimzi\n"` |  |
| argo-cd.server.config."resource.compareoptions" | string | `"ignoreAggregatedRoles: true\n"` |  |
| argo-cd.server.config.url | string | Set by Argo CD | Injected by ArgoCD; do not set in the individual environment files |
| argo-cd.server.extraArgs[0] | string | `"--basehref=/argo-cd"` |  |
| argo-cd.server.extraArgs[1] | string | `"--insecure=true"` |  |
| argo-cd.server.ingress.annotations."kubernetes.io/ingress.class" | string | `"nginx"` |  |
| argo-cd.server.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| argo-cd.server.ingress.enabled | bool | `true` |  |
| argo-cd.server.ingress.host | list | Set by Argo CD | Injected by ArgoCD; do not set in the individual environment files |
| argo-cd.server.ingress.paths[0] | string | `"/argo-cd(/|$)(.*)"` |  |
| argo-cd.server.metrics.enabled | bool | `true` |  |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| vault_secret.enabled | bool | `true` |  |
| vault_secret.path | string | `""` |  |
