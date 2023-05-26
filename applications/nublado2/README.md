# nublado2

![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square) ![AppVersion: 2.6.1](https://img.shields.io/badge/AppVersion-2.6.1-informational?style=flat-square)

JupyterHub for the Rubin Science Platform

**Homepage:** <https://github.com/lsst-sqre/nublado2>

## Source Code

* <https://github.com/lsst-sqre/nublado2>

## Requirements

Kubernetes: `>=1.20.0-0`

| Repository | Name | Version |
|------------|------|---------|
| https://jupyterhub.github.io/helm-chart/ | jupyterhub | 2.0.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.base_url | string | `""` | base_url must be set in each instantiation of this chart to the URL of the primary ingress.  It's used to construct API requests to the authentication service (which should go through the ingress). |
| config.butler_secret_path | string | `""` | butler_secret_path must be set here, because it's passed through to the lab rather than being part of the Hub configuration. |
| config.cachemachine_image_policy | string | `"available"` | Cachemachine image policy: "available" or "desired".  Use "desired" at instances with streaming image support. |
| config.lab_environment | object | See `values.yaml` | Environment variables to set in spawned lab containers. Each value will be expanded using Jinja 2 templating. |
| config.pinned_images | list | `[]` | images to pin to spawner menu |
| config.pull_secret_path | string | `""` | pull_secret_path must also be set here; it specifies resources in the lab namespace |
| config.shutdown_on_logout | bool | `true` | shut down user pods on logout.  Superfluous, because our LogoutHandler enforces this in any event, but nice to make explicit. |
| config.sizes | list | `[{"cpu":1,"name":"Small","ram":"3072M"},{"cpu":2,"name":"Medium","ram":"6144M"},{"cpu":4,"name":"Large","ram":"12288M"}]` | definitions of Lab sizes available in a given instance |
| config.user_resources_template | string | See `values.yaml` | Templates for the user resources to create for each lab spawn. This is a string that can be templated and then loaded as YAML to generate a list of Kubernetes objects to create. |
| config.volume_mounts | list | `[]` | Where to mount volumes for a particular instance |
| config.volumes | list | `[]` | Volumes to use for a particular instance |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| jupyterhub.cull.enabled | bool | `true` |  |
| jupyterhub.cull.every | int | `600` |  |
| jupyterhub.cull.maxAge | int | `5184000` |  |
| jupyterhub.cull.removeNamedServers | bool | `true` |  |
| jupyterhub.cull.timeout | int | `2592000` |  |
| jupyterhub.cull.users | bool | `true` |  |
| jupyterhub.hub.authenticatePrometheus | bool | `false` |  |
| jupyterhub.hub.baseUrl | string | `"/nb"` |  |
| jupyterhub.hub.config.Authenticator.enable_auth_state | bool | `true` |  |
| jupyterhub.hub.config.JupyterHub.authenticator_class | string | `"nublado2.auth.GafaelfawrAuthenticator"` |  |
| jupyterhub.hub.config.ServerApp.shutdown_no_activity_timeout | int | `604800` |  |
| jupyterhub.hub.containerSecurityContext.allowPrivilegeEscalation | bool | `false` |  |
| jupyterhub.hub.containerSecurityContext.runAsGroup | int | `768` |  |
| jupyterhub.hub.containerSecurityContext.runAsUser | int | `768` |  |
| jupyterhub.hub.db.password | string | `"true"` |  |
| jupyterhub.hub.db.type | string | `"postgres"` |  |
| jupyterhub.hub.db.url | string | `"postgresql://jovyan@postgres.postgres/jupyterhub"` |  |
| jupyterhub.hub.existingSecret | string | `"nublado2-secret"` |  |
| jupyterhub.hub.extraConfig."nublado.py" | string | `"import nublado2.hub_config\nnublado2.hub_config.HubConfig().configure(c)\n"` |  |
| jupyterhub.hub.extraVolumeMounts[0].mountPath | string | `"/etc/jupyterhub/nublado_config.yaml"` |  |
| jupyterhub.hub.extraVolumeMounts[0].name | string | `"nublado-config"` |  |
| jupyterhub.hub.extraVolumeMounts[0].subPath | string | `"nublado_config.yaml"` |  |
| jupyterhub.hub.extraVolumeMounts[1].mountPath | string | `"/etc/keys/gafaelfawr-token"` |  |
| jupyterhub.hub.extraVolumeMounts[1].name | string | `"nublado-gafaelfawr"` |  |
| jupyterhub.hub.extraVolumeMounts[1].subPath | string | `"token"` |  |
| jupyterhub.hub.extraVolumes[0].configMap.name | string | `"nublado-config"` |  |
| jupyterhub.hub.extraVolumes[0].name | string | `"nublado-config"` |  |
| jupyterhub.hub.extraVolumes[1].name | string | `"nublado-gafaelfawr"` |  |
| jupyterhub.hub.extraVolumes[1].secret.secretName | string | `"gafaelfawr-token"` |  |
| jupyterhub.hub.image.name | string | `"lsstsqre/nublado2"` |  |
| jupyterhub.hub.image.tag | string | `"2.6.1"` |  |
| jupyterhub.hub.loadRoles.self.scopes[0] | string | `"admin:servers!user"` |  |
| jupyterhub.hub.loadRoles.self.scopes[1] | string | `"read:metrics"` |  |
| jupyterhub.hub.loadRoles.server.scopes[0] | string | `"inherit"` |  |
| jupyterhub.hub.networkPolicy.enabled | bool | `false` |  |
| jupyterhub.hub.resources.limits.cpu | string | `"900m"` |  |
| jupyterhub.hub.resources.limits.memory | string | `"1Gi"` |  |
| jupyterhub.imagePullSecrets[0].name | string | `"pull-secret"` |  |
| jupyterhub.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the ingress |
| jupyterhub.ingress.enabled | bool | `true` |  |
| jupyterhub.ingress.ingressClassName | string | `"nginx"` |  |
| jupyterhub.ingress.pathSuffix | string | `"*"` |  |
| jupyterhub.prePuller.continuous.enabled | bool | `false` |  |
| jupyterhub.prePuller.hook.enabled | bool | `false` |  |
| jupyterhub.proxy.chp.networkPolicy.interNamespaceAccessLabels | string | `"accept"` |  |
| jupyterhub.proxy.service.type | string | `"ClusterIP"` |  |
| jupyterhub.scheduling.userPlaceholder.enabled | bool | `false` |  |
| jupyterhub.scheduling.userScheduler.enabled | bool | `false` |  |
| jupyterhub.singleuser.cloudMetadata.blockWithIptables | bool | `false` |  |
| jupyterhub.singleuser.cmd | string | `"/opt/lsst/software/jupyterlab/runlab.sh"` |  |
| jupyterhub.singleuser.defaultUrl | string | `"/lab"` |  |
| jupyterhub.singleuser.extraAnnotations."argocd.argoproj.io/compare-options" | string | `"IgnoreExtraneous"` |  |
| jupyterhub.singleuser.extraAnnotations."argocd.argoproj.io/sync-options" | string | `"Prune=false"` |  |
| jupyterhub.singleuser.extraLabels."argocd.argoproj.io/instance" | string | `"nublado-users"` |  |
| jupyterhub.singleuser.extraLabels."hub.jupyter.org/network-access-hub" | string | `"true"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[0].mountPath | string | `"/etc/dask"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[0].name | string | `"dask"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[1].mountPath | string | `"/opt/lsst/software/jupyterlab/panda"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[1].name | string | `"idds-config"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[2].mountPath | string | `"/tmp"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[2].name | string | `"tmp"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[3].mountPath | string | `"/opt/lsst/software/jupyterlab/butler-secret"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[3].name | string | `"butler-secret"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[4].mountPath | string | `"/opt/lsst/software/jupyterlab/environment"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[4].name | string | `"lab-environment"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[5].mountPath | string | `"/etc/passwd"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[5].name | string | `"passwd"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[5].readOnly | bool | `true` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[5].subPath | string | `"passwd"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[6].mountPath | string | `"/etc/group"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[6].name | string | `"group"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[6].readOnly | bool | `true` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[6].subPath | string | `"group"` |  |
| jupyterhub.singleuser.storage.extraVolumes[0].configMap.name | string | `"dask"` |  |
| jupyterhub.singleuser.storage.extraVolumes[0].name | string | `"dask"` |  |
| jupyterhub.singleuser.storage.extraVolumes[1].configMap.name | string | `"idds-config"` |  |
| jupyterhub.singleuser.storage.extraVolumes[1].name | string | `"idds-config"` |  |
| jupyterhub.singleuser.storage.extraVolumes[2].emptyDir | object | `{}` |  |
| jupyterhub.singleuser.storage.extraVolumes[2].name | string | `"tmp"` |  |
| jupyterhub.singleuser.storage.extraVolumes[3].name | string | `"butler-secret"` |  |
| jupyterhub.singleuser.storage.extraVolumes[3].secret.secretName | string | `"butler-secret"` |  |
| jupyterhub.singleuser.storage.extraVolumes[4].configMap.defaultMode | int | `420` |  |
| jupyterhub.singleuser.storage.extraVolumes[4].configMap.name | string | `"lab-environment"` |  |
| jupyterhub.singleuser.storage.extraVolumes[4].name | string | `"lab-environment"` |  |
| jupyterhub.singleuser.storage.extraVolumes[5].configMap.defaultMode | int | `420` |  |
| jupyterhub.singleuser.storage.extraVolumes[5].configMap.name | string | `"passwd"` |  |
| jupyterhub.singleuser.storage.extraVolumes[5].name | string | `"passwd"` |  |
| jupyterhub.singleuser.storage.extraVolumes[6].configMap.defaultMode | int | `420` |  |
| jupyterhub.singleuser.storage.extraVolumes[6].configMap.name | string | `"group"` |  |
| jupyterhub.singleuser.storage.extraVolumes[6].name | string | `"group"` |  |
| jupyterhub.singleuser.storage.type | string | `"none"` |  |
| network_policy.enabled | bool | `true` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)
