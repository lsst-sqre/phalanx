# nublado2

Nublado2 JupyterHub installation

**Homepage:** <https://github.com/lsst-sqre/nublado2>

## Source Code

* <https://github.com/lsst-sqre/nublado2>

## Requirements

Kubernetes: `>=1.20.0-0`

| Repository | Name | Version |
|------------|------|---------|
| https://jupyterhub.github.io/helm-chart/ | jupyterhub | 1.1.3-n474.h8d0a7616 |
| https://lsst-sqre.github.io/charts/ | pull-secret | 0.1.2 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.base_url | string | `""` |  |
| config.butler_secret_path | string | `""` |  |
| config.cachemachine_image_policy | string | `"available"` |  |
| config.lab_environment | object | See `values.yaml` | Environment variables to set in spawned lab containers. Each value will be expanded using Jinja 2 templating. |
| config.pinned_images | list | `[]` |  |
| config.pull_secret_path | string | `""` |  |
| config.sizes[0].cpu | int | `1` |  |
| config.sizes[0].name | string | `"Small"` |  |
| config.sizes[0].ram | string | `"3072M"` |  |
| config.sizes[1].cpu | int | `2` |  |
| config.sizes[1].name | string | `"Medium"` |  |
| config.sizes[1].ram | string | `"6144M"` |  |
| config.sizes[2].cpu | int | `4` |  |
| config.sizes[2].name | string | `"Large"` |  |
| config.sizes[2].ram | string | `"12288M"` |  |
| config.user_resources_template | string | See `values.yaml` | Templates for the user resources to create for each lab spawn. This is a string that can be templated and then loaded as YAML to generate a list of Kubernetes objects to create. |
| config.volume_mounts | list | `[]` |  |
| config.volumes | list | `[]` |  |
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
| jupyterhub.hub.image.tag | string | `"2.1.0"` |  |
| jupyterhub.hub.loadRoles.self.scopes[0] | string | `"admin:servers!user"` |  |
| jupyterhub.hub.loadRoles.self.scopes[1] | string | `"read:metrics"` |  |
| jupyterhub.hub.loadRoles.server.scopes[0] | string | `"inherit"` |  |
| jupyterhub.hub.networkPolicy.enabled | bool | `false` |  |
| jupyterhub.imagePullSecrets[0].name | string | `"pull-secret"` |  |
| jupyterhub.ingress.annotations."kubernetes.io/ingress.class" | string | `"nginx"` |  |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/auth-method" | string | `"GET"` |  |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/auth-response-headers" | string | `"X-Auth-Request-Token"` |  |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/auth-url" | string | `"http://gafaelfawr.gafaelfawr.svc.cluster.local:8080/auth?scope=exec:notebook&notebook=true"` |  |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/configuration-snippet" | string | `"error_page 403 = \"/auth/forbidden?scope=exec:notebook\";\n"` |  |
| jupyterhub.ingress.enabled | bool | `true` |  |
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
| jupyterhub.singleuser.storage.extraVolumeMounts[7].mountPath | string | `"/etc/shadow"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[7].name | string | `"shadow"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[7].readOnly | bool | `true` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[7].subPath | string | `"shadow"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[8].mountPath | string | `"/etc/gshadow"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[8].name | string | `"gshadow"` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[8].readOnly | bool | `true` |  |
| jupyterhub.singleuser.storage.extraVolumeMounts[8].subPath | string | `"gshadow"` |  |
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
| jupyterhub.singleuser.storage.extraVolumes[7].configMap.defaultMode | int | `384` |  |
| jupyterhub.singleuser.storage.extraVolumes[7].configMap.name | string | `"shadow"` |  |
| jupyterhub.singleuser.storage.extraVolumes[7].name | string | `"shadow"` |  |
| jupyterhub.singleuser.storage.extraVolumes[8].configMap.defaultMode | int | `384` |  |
| jupyterhub.singleuser.storage.extraVolumes[8].configMap.name | string | `"gshadow"` |  |
| jupyterhub.singleuser.storage.extraVolumes[8].name | string | `"gshadow"` |  |
| jupyterhub.singleuser.storage.type | string | `"none"` |  |
| network_policy.enabled | bool | `true` |  |
| vault_secret_path | string | `""` |  |
