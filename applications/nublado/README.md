# nublado

JupyterHub and custom spawner for the Rubin Science Platform

**Homepage:** <https://github.com/lsst-sqre/jupyterlab-controller>

## Source Code

* <https://github.com/lsst-sqre/jupyterlab-controller>
* <https://github.com/lsst-sqre/rsp-restspawner>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| controller.affinity | object | `{}` | Affinity rules for the lab controller pod |
| controller.config.images.aliasTags | list | `[]` | Additional tags besides `recommendedTag` that should be recognized as aliases. |
| controller.config.images.cycle | string | `nil` | Restrict images to this SAL cycle, if given. |
| controller.config.images.numDailies | int | `3` | Number of most-recent dailies to prepull. |
| controller.config.images.numReleases | int | `1` | Number of most-recent releases to prepull. |
| controller.config.images.numWeeklies | int | `2` | Number of most-recent weeklies to prepull. |
| controller.config.images.pin | list | `[]` | List of additional image tags to prepull. Listing the image tagged as recommended here is recommended when using a Docker image source to ensure its name can be expanded properly in the menu. |
| controller.config.images.recommendedTag | string | `"recommended"` | Tag marking the recommended image (shown first in the menu) |
| controller.config.images.source | object | None, must be specified | Source for prepulled images. For Docker, set `type` to `docker`, `registry` to the hostname and `repository` to the name of the repository. For Google Artifact Repository, set `type` to `google`, `location` to the region, `projectId` to the Google project, `repository` to the name of the repository, and `image` to the name of the image. |
| controller.config.lab.env | object | See `values.yaml` | Environment variables to set for every user lab. |
| controller.config.lab.files | object | See `values.yaml` | Files to be mounted as ConfigMaps inside the user lab pod. `contents` contains the file contents. Set `modify` to true to make the file writable in the pod. |
| controller.config.lab.initcontainers | list | `[]` | Containers run as init containers with each user pod. Each should set `name`, `image` (a Docker image reference), and `privileged`, and may contain `volumes` (similar to the main `volumes` configuration). If `privileged` is true, the container will run as root with `allowPrivilegeEscalation` true. Otherwise it will, run as UID 1000. |
| controller.config.lab.secrets | list | `[]` | Secrets to set in the user pods. Each should have a `secretKey` key pointing to a secret in the same namespace as the controller (generally `nublado-secret`) and `secretRef` pointing to a field in that key. |
| controller.config.lab.sizes | object | See `values.yaml` (specifies `small`, `medium`, and | Available lab sizes. Names must be chosen from `fine`, `diminutive`, `tiny`, `small`, `medium`, `large`, `huge`, `gargantuan`, and `colossal` in that order. Each should specify the maximum CPU equivalents and memory. SI prefixes for memory are supported. `large`) |
| controller.config.lab.volumes | object | `{}` | Volumes that should be mounted in lab pods. Currently this only supports NFS volumes and must specify `containerPath`, `server`, `serverPath`, and `mode` where mode is one of `ro` or `rw`. |
| controller.config.safir.logLevel | string | `"INFO"` | Level of Python logging |
| controller.config.safir.pathPrefix | string | `"/nublado"` | Path prefix that will be routed to the controller |
| controller.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the nublado image |
| controller.image.repository | string | `"ghcr.io/lsst-sqre/jupyterlab-controller"` | nublado image to use |
| controller.image.tag | string | The appVersion of the chart | Tag of nublado image to use |
| controller.ingress.annotations | object | `{}` | Additional annotations to add for the lab controller pod ingress |
| controller.nodeSelector | object | `{}` | Node selector rules for the lab controller pod |
| controller.podAnnotations | object | `{}` | Annotations for the lab controller pod |
| controller.resources | object | `{}` | Resource limits and requests for the lab controller pod |
| controller.tolerations | list | `[]` | Tolerations for the lab controller pod |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| jupyterhub.cull.enabled | bool | `true` |  |
| jupyterhub.cull.every | int | `600` |  |
| jupyterhub.cull.maxAge | int | `5184000` |  |
| jupyterhub.cull.removeNamedServers | bool | `true` |  |
| jupyterhub.cull.timeout | int | `2592000` |  |
| jupyterhub.cull.users | bool | `true` |  |
| jupyterhub.hub.authenticatePrometheus | bool | `false` |  |
| jupyterhub.hub.baseUrl | string | `"/nb"` |  |
| jupyterhub.hub.containerSecurityContext.allowPrivilegeEscalation | bool | `false` |  |
| jupyterhub.hub.containerSecurityContext.runAsGroup | int | `768` |  |
| jupyterhub.hub.containerSecurityContext.runAsUser | int | `768` |  |
| jupyterhub.hub.db.password | string | `"true"` |  |
| jupyterhub.hub.db.type | string | `"postgres"` |  |
| jupyterhub.hub.db.url | string | `"postgresql://jovyan@postgres.postgres/jupyterhub"` |  |
| jupyterhub.hub.existingSecret | string | `"nublado-secret"` |  |
| jupyterhub.hub.extraEnv.JUPYTERHUB_CRYPT_KEY.valueFrom.secretKeyRef.key | string | `"hub.config.CryptKeeper.keys"` |  |
| jupyterhub.hub.extraEnv.JUPYTERHUB_CRYPT_KEY.valueFrom.secretKeyRef.name | string | `"nublado-secret"` |  |
| jupyterhub.hub.extraVolumeMounts[0].mountPath | string | `"/usr/local/etc/jupyterhub/jupyterhub_config.d"` |  |
| jupyterhub.hub.extraVolumeMounts[0].name | string | `"hub-config"` |  |
| jupyterhub.hub.extraVolumeMounts[1].mountPath | string | `"/etc/gafaelfawr"` |  |
| jupyterhub.hub.extraVolumeMounts[1].name | string | `"hub-gafaelfawr-token"` |  |
| jupyterhub.hub.extraVolumes[0].configMap.name | string | `"hub-config"` |  |
| jupyterhub.hub.extraVolumes[0].name | string | `"hub-config"` |  |
| jupyterhub.hub.extraVolumes[1].name | string | `"hub-gafaelfawr-token"` |  |
| jupyterhub.hub.extraVolumes[1].secret.secretName | string | `"hub-gafaelfawr-token"` |  |
| jupyterhub.hub.image.name | string | `"ghcr.io/lsst-sqre/rsp-restspawner"` |  |
| jupyterhub.hub.image.tag | string | `"0.1.2"` |  |
| jupyterhub.hub.loadRoles.self.scopes[0] | string | `"admin:servers!user"` |  |
| jupyterhub.hub.loadRoles.self.scopes[1] | string | `"read:metrics"` |  |
| jupyterhub.hub.loadRoles.server.scopes[0] | string | `"inherit"` |  |
| jupyterhub.hub.networkPolicy.enabled | bool | `false` |  |
| jupyterhub.hub.resources.limits.cpu | string | `"900m"` |  |
| jupyterhub.hub.resources.limits.memory | string | `"1Gi"` |  |
| jupyterhub.ingress.enabled | bool | `false` |  |
| jupyterhub.prePuller.continuous.enabled | bool | `false` |  |
| jupyterhub.prePuller.hook.enabled | bool | `false` |  |
| jupyterhub.proxy.chp.networkPolicy.interNamespaceAccessLabels | string | `"accept"` |  |
| jupyterhub.proxy.service.type | string | `"ClusterIP"` |  |
| jupyterhub.scheduling.userPlaceholder.enabled | bool | `false` |  |
| jupyterhub.scheduling.userScheduler.enabled | bool | `false` |  |
| jupyterhub.singleuser.cloudMetadata.blockWithIptables | bool | `false` |  |
| jupyterhub.singleuser.cmd | string | `"/opt/lsst/software/jupyterlab/runlab.sh"` |  |
| jupyterhub.singleuser.defaultUrl | string | `"/lab"` |  |
