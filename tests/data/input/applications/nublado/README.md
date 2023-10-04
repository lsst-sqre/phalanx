# nublado

![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square) ![AppVersion: 0.7.1](https://img.shields.io/badge/AppVersion-0.7.1-informational?style=flat-square)

JupyterHub and custom spawner for the Rubin Science Platform

**Homepage:** <https://github.com/lsst-sqre/jupyterlab-controller>

## Source Code

* <https://github.com/lsst-sqre/jupyterlab-controller>
* <https://github.com/lsst-sqre/rsp-restspawner>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://jupyterhub.github.io/helm-chart/ | jupyterhub | 2.0.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| controller.affinity | object | `{}` | Affinity rules for the lab controller pod |
| controller.config.fileserver.enabled | bool | `false` | Enable fileserver management |
| controller.config.fileserver.image | string | `"ghcr.io/lsst-sqre/worblehat"` | Image for fileserver container |
| controller.config.fileserver.namespace | string | `"fileservers"` | Namespace for user fileservers |
| controller.config.fileserver.pullPolicy | string | `"IfNotPresent"` | Pull policy for fileserver container |
| controller.config.fileserver.tag | string | `"0.1.0"` | Tag for fileserver container |
| controller.config.fileserver.timeout | int | `3600` | Timeout for user fileservers, in seconds |
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
| controller.config.lab.pullSecret | string | Do not use a pull secret | Pull secret to use for labs. Set to the string `pull-secret` to use the normal pull secret from Vault. |
| controller.config.lab.secrets | list | `[]` | Secrets to set in the user pods. Each should have a `secretKey` key pointing to a secret in the same namespace as the controller (generally `nublado-secret`) and `secretRef` pointing to a field in that key. |
| controller.config.lab.sizes | object | See `values.yaml` (specifies `small`, `medium`, and | Available lab sizes. Names must be chosen from `fine`, `diminutive`, `tiny`, `small`, `medium`, `large`, `huge`, `gargantuan`, and `colossal` in that order. Each should specify the maximum CPU equivalents and memory. SI prefixes for memory are supported. `large`) |
| controller.config.lab.volumes | list | `[]` | Volumes that should be mounted in lab pods. This supports NFS, HostPath, and PVC volume types (differentiated in source.type) |
| controller.config.safir.logLevel | string | `"INFO"` | Level of Python logging |
| controller.config.safir.pathPrefix | string | `"/nublado"` | Path prefix that will be routed to the controller |
| controller.googleServiceAccount | string | None, must be set when using Google Artifact Registry | If Google Artifact Registry is used as the image source, the Google service account that has an IAM binding to the `nublado-controller` Kubernetes service account and has the Artifact Registry reader role |
| controller.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the nublado image |
| controller.image.repository | string | `"ghcr.io/lsst-sqre/jupyterlab-controller"` | nublado image to use |
| controller.image.tag | string | The appVersion of the chart | Tag of nublado image to use |
| controller.ingress.annotations | object | `{}` | Additional annotations to add for the lab controller pod ingress |
| controller.nodeSelector | object | `{}` | Node selector rules for the lab controller pod |
| controller.podAnnotations | object | `{}` | Annotations for the lab controller pod |
| controller.resources | object | `{}` | Resource limits and requests for the lab controller pod |
| controller.slackAlerts | bool | `false` | Whether to enable Slack alerts. If set to true, `slack_webhook` must be set in the corresponding Nublado Vault secret. |
| controller.tolerations | list | `[]` | Tolerations for the lab controller pod |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| hub.internalDatabase | bool | `true` | Whether to use the cluster-internal PostgreSQL server instead of an external server. This is not used directly by the Nublado chart, but controls how the database password is managed. |
| hub.timeout.spawn | int | `600` | Timeout for the Kubernetes spawn process in seconds. (Allow long enough to pull uncached images if needed.) |
| hub.timeout.startup | int | `90` | Timeout for JupyterLab to start. Currently this sometimes takes over 60 seconds for reasons we don't understand. |
| jupyterhub.cull.enabled | bool | `true` | Enable the lab culler. |
| jupyterhub.cull.every | int | 600 (10 minutes) | How frequently to check for idle labs in seconds |
| jupyterhub.cull.maxAge | int | 5184000 (60 days) | Maximum age of a lab regardless of activity |
| jupyterhub.cull.removeNamedServers | bool | `true` | Whether to remove named servers when culling their lab |
| jupyterhub.cull.timeout | int | 2592000 (30 days) | Default idle timeout before the lab is automatically deleted in seconds |
| jupyterhub.cull.users | bool | `true` | Whether to log out the server when culling their lab |
| jupyterhub.hub.authenticatePrometheus | bool | `false` | Whether to require metrics requests to be authenticated |
| jupyterhub.hub.baseUrl | string | `"/nb"` | Base URL on which JupyterHub listens |
| jupyterhub.hub.containerSecurityContext | object | `{"allowPrivilegeEscalation":false,"runAsGroup":768,"runAsUser":768}` | Security context for JupyterHub container |
| jupyterhub.hub.db.password | string | Comes from nublado-secret | Database password (not used) |
| jupyterhub.hub.db.type | string | `"postgres"` | Type of database to use |
| jupyterhub.hub.db.url | string | Use the in-cluster PostgreSQL installed by Phalanx | URL of PostgreSQL server |
| jupyterhub.hub.existingSecret | string | `"nublado-secret"` | Existing secret to use for private keys |
| jupyterhub.hub.extraEnv | object | Gets `JUPYTERHUB_CRYPT_KEY` from `nublado-secret` | Additional environment variables to set |
| jupyterhub.hub.extraVolumeMounts | list | `hub-config` and the Gafaelfawr token | Additional volume mounts for JupyterHub |
| jupyterhub.hub.extraVolumes | list | The `hub-config` `ConfigMap` and the Gafaelfawr token | Additional volumes to make available to JupyterHub |
| jupyterhub.hub.image.name | string | `"ghcr.io/lsst-sqre/rsp-restspawner"` | Image to use for JupyterHub |
| jupyterhub.hub.image.tag | string | `"0.3.2"` | Tag of image to use for JupyterHub |
| jupyterhub.hub.loadRoles.server.scopes | list | `["self"]` | Default scopes for the user's lab, overridden to allow the lab to delete itself (which we use for our added menu items) |
| jupyterhub.hub.networkPolicy.enabled | bool | `false` | Whether to enable the default `NetworkPolicy` (currently, the upstream one does not work correctly) |
| jupyterhub.hub.resources | object | `{"limits":{"cpu":"900m","memory":"1Gi"}}` | Resource limits and requests |
| jupyterhub.ingress.enabled | bool | `false` | Whether to enable the default ingress |
| jupyterhub.prePuller.continuous.enabled | bool | `false` | Whether to run the JupyterHub continuous prepuller (the Nublado controller does its own prepulling) |
| jupyterhub.prePuller.hook.enabled | bool | `false` | Whether to run the JupyterHub hook prepuller (the Nublado controller does its own prepulling) |
| jupyterhub.proxy.chp.networkPolicy.interNamespaceAccessLabels | string | `"accept"` | Enable access to the proxy from other namespaces, since we put each user's lab environment in its own namespace |
| jupyterhub.proxy.service.type | string | `"ClusterIP"` | Only expose the proxy to the cluster, overriding the default of exposing the proxy directly to the Internet |
| jupyterhub.scheduling.userPlaceholder.enabled | bool | `false` | Whether to spawn placeholder pods representing fake users to force autoscaling in advance of running out of resources |
| jupyterhub.scheduling.userScheduler.enabled | bool | `false` | Whether the user scheduler should be enabled |
| jupyterhub.singleuser.cloudMetadata.blockWithIptables | bool | `false` | Whether to configure iptables to block cloud metadata endpoints. This is unnecessary in our environments (they are blocked by cluster configuration) and thus is disabled to reduce complexity. |
| jupyterhub.singleuser.cmd | string | `"/opt/lsst/software/jupyterlab/runlab.sh"` | Start command for labs |
| jupyterhub.singleuser.defaultUrl | string | `"/lab"` | Default URL prefix for lab endpoints |
| proxy.ingress.annotations | object | Increase `proxy-read-timeout` and `proxy-send-timeout` to 5m | Additional annotations to add to the proxy ingress (also used to talk to JupyterHub and all user labs) |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)
