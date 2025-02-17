# nublado

JupyterHub and custom spawner for the Rubin Science Platform

**Homepage:** <https://nublado.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/nublado>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cloudsql.affinity | object | `{}` | Affinity rules for the Cloud SQL Auth Proxy pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.resources | object | See `values.yaml` | Resource requests and limits for Cloud SQL pod |
| cloudsql.image.tag | string | `"1.37.4"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | None, must be set if Cloud SQL Auth Proxy is enabled | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.nodeSelector | object | `{}` | Node selection rules for the Cloud SQL Auth Proxy pod |
| cloudsql.podAnnotations | object | `{}` | Annotations for the Cloud SQL Auth Proxy pod |
| cloudsql.resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy pod |
| cloudsql.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the `cloud-sql-proxy` Kubernetes service account and has the `cloudsql.client` role |
| cloudsql.tolerations | list | `[]` | Tolerations for the Cloud SQL Auth Proxy pod |
| controller.affinity | object | `{}` | Affinity rules for the Nublado controller |
| controller.config.fileserver.affinity | object | `{}` | Affinity rules for user file server pods |
| controller.config.fileserver.application | string | `"nublado-fileservers"` | Argo CD application in which to collect user file servers |
| controller.config.fileserver.creationTimeout | string | `"2m"` | Timeout to wait for Kubernetes to create file servers, in Safir `parse_timedelta` format |
| controller.config.fileserver.deleteTimeout | string | `"1m"` | Timeout for deleting a user's file server from Kubernetes, in Safir `parse_timedelta` format |
| controller.config.fileserver.enabled | bool | `false` | Enable user file servers |
| controller.config.fileserver.idleTimeout | string | `"1h"` | Timeout for idle user fileservers, in Safir `parse_timedelta` format |
| controller.config.fileserver.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for file server image |
| controller.config.fileserver.image.repository | string | `"ghcr.io/lsst-sqre/worblehat"` | File server image to use |
| controller.config.fileserver.image.tag | string | `"0.1.0"` | Tag of file server image to use |
| controller.config.fileserver.namespace | string | `"fileservers"` | Namespace for user file servers |
| controller.config.fileserver.nodeSelector | object | `{}` | Node selector rules for user file server pods |
| controller.config.fileserver.pathPrefix | string | `"/files"` | Path prefix for user file servers |
| controller.config.fileserver.resources | object | See `values.yaml` | Resource requests and limits for user file servers |
| controller.config.fileserver.tolerations | list | `[]` | Tolerations for user file server pods |
| controller.config.fileserver.volumeMounts | list | `[]` | Volumes that should be made available via WebDAV |
| controller.config.images.aliasTags | list | `[]` | Additional tags besides `recommendedTag` that should be recognized as aliases. |
| controller.config.images.cycle | string | `nil` | Restrict images to this SAL cycle, if given. |
| controller.config.images.numDailies | int | `3` | Number of most-recent dailies to prepull. |
| controller.config.images.numReleases | int | `1` | Number of most-recent releases to prepull. |
| controller.config.images.numWeeklies | int | `2` | Number of most-recent weeklies to prepull. |
| controller.config.images.pin | list | `[]` | List of additional image tags to prepull. Listing the image tagged as recommended here is recommended when using a Docker image source to ensure its name can be expanded properly in the menu. |
| controller.config.images.recommendedTag | string | `"recommended"` | Tag marking the recommended image (shown first in the menu) |
| controller.config.images.source | object | None, must be specified | Source for prepulled images. For Docker, set `type` to `docker`, `registry` to the hostname and `repository` to the name of the repository. For Google Artifact Repository, set `type` to `google`, `location` to the region, `projectId` to the Google project, `repository` to the name of the repository, and `image` to the name of the image. |
| controller.config.lab.affinity | object | `{}` | Affinity rules for user lab pods |
| controller.config.lab.application | string | `"nublado-users"` | Argo CD application in which to collect user lab objects |
| controller.config.lab.deleteTimeout | string | `"1m"` | Timeout for deleting a user's lab resources from Kubernetes in Safir `parse_timedelta` format |
| controller.config.lab.env | object | See `values.yaml` | Environment variables to set for every user lab |
| controller.config.lab.extraAnnotations | object | `{}` | Extra annotations to add to user lab pods |
| controller.config.lab.files | object | See `values.yaml` | Files to be mounted as ConfigMaps inside the user lab pod. `contents` contains the file contents. Set `modify` to true to make the file writable in the pod. |
| controller.config.lab.homedirPrefix | string | `"/home"` | Prefix of home directory path to add before the username. This is the path inside the container, not the path of the volume. |
| controller.config.lab.homedirSchema | string | `"username"` | Schema for home directory construction. Choose between `username` (paths like `/home/rachel`) and `initialThenUsername` (paths like `/home/r/rachel`). |
| controller.config.lab.homedirSuffix | string | `""` | Portion of the home directory path after the username. This is intended for environments that want the JupyterLab home directory to be a subdirectory of the user's home directory in some external environment. |
| controller.config.lab.initContainers | list | `[]` | Containers run as init containers with each user pod. Each should set `name`, `image` (a Docker image and pull policy specification), and `privileged`, and may contain `volumeMounts` (similar to the main `volumeMountss` configuration). If `privileged` is true, the container will run as root with all capabilities. Otherwise it will run as the user. |
| controller.config.lab.jupyterlabConfigDir | string | `"/opt/lsst/software/jupyterlab"` | Path inside the lab container where custom JupyterLab configuration is stored |
| controller.config.lab.labStartCommand | list | `["/opt/lsst/software/jupyterlab/runlab.sh"]` | Command executed in the container to start the lab |
| controller.config.lab.namespacePrefix | string | `"nublado"` | Prefix for namespaces for user labs. To this will be added a dash (`-`) and the user's username. |
| controller.config.lab.nodeSelector | object | `{}` | Node selector rules for user lab pods |
| controller.config.lab.nss.baseGroup | string | See `values.yaml` | Base `/etc/group` file for lab containers |
| controller.config.lab.nss.basePasswd | string | See `values.yaml` | Base `/etc/passwd` file for lab containers |
| controller.config.lab.pullSecret | string | Do not use a pull secret | Pull secret to use for labs. Set to the string `pull-secret` to use the normal pull secret from Vault. |
| controller.config.lab.runtimeMountsDir | string | `"/opt/lsst/software/jupyterlab"` | Directory in the lab under which runtime information such as tokens, environment variables, and container information will be mounted |
| controller.config.lab.secrets | list | `[]` | Secrets to set in the user pods. Each should have a `secretKey` key pointing to a secret in the same namespace as the controller (generally `nublado-secret`) and `secretRef` pointing to a field in that key. |
| controller.config.lab.sizes | list | See `values.yaml` | Available lab sizes. Sizes must be chosen from `fine`, `diminutive`, `tiny`, `small`, `medium`, `large`, `huge`, `gargantuan`, and `colossal` in that order. Each should specify the maximum CPU equivalents and memory. SI suffixes for memory are supported. Sizes will be shown in the order defined here, and the first defined size will be the default. |
| controller.config.lab.spawnTimeout | int | `600` | How long to wait for Kubernetes to spawn a lab in seconds. This should generally be shorter than the spawn timeout set in JupyterHub. |
| controller.config.lab.tmpSource | string | `"memory"` | Select where `/tmp` in the lab will come from. Choose between `disk` (node-local ephemeral storage) and `memory` (tmpfs capped at 25% of the available memory). |
| controller.config.lab.tolerations | list | `[]` | Tolerations for user lab pods |
| controller.config.lab.volumeMounts | list | `[]` | Volumes that should be mounted in lab pods. |
| controller.config.lab.volumes | list | `[]` | Volumes that will be in lab pods or init containers. This supports NFS, HostPath, and PVC volume types (differentiated in source.type). |
| controller.config.logLevel | string | `"INFO"` | Level of Python logging |
| controller.config.metrics.application | string | `"nublado"` | Name under which to log metrics. Generally there is no reason to change this. |
| controller.config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| controller.config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| controller.config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| controller.config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| controller.config.pathPrefix | string | `"/nublado"` | Path prefix that will be routed to the controller |
| controller.googleServiceAccount | string | None, must be set when using Google Artifact Registry | If Google Artifact Registry is used as the image source, the Google service account that has an IAM binding to the `nublado-controller` Kubernetes service account and has the Artifact Registry reader role |
| controller.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the controller image |
| controller.image.repository | string | `"ghcr.io/lsst-sqre/nublado-controller"` | Nublado controller image to use |
| controller.image.tag | string | The appVersion of the chart | Tag of Nublado controller image to use |
| controller.ingress.annotations | object | `{}` | Additional annotations to add for the Nublado controller ingress |
| controller.nodeSelector | object | `{}` | Node selector rules for the Nublado controller |
| controller.podAnnotations | object | `{}` | Annotations for the Nublado controller |
| controller.resources | object | See `values.yaml` | Resource limits and requests for the Nublado controller |
| controller.slackAlerts | bool | `false` | Whether to enable Slack alerts. If set to true, `slack_webhook` must be set in the corresponding Nublado Vault secret. |
| controller.tolerations | list | `[]` | Tolerations for the Nublado controller |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| hub.internalDatabase | bool | `false` | Whether to use the cluster-internal PostgreSQL server instead of an external server. This is not used directly by the Nublado chart, but controls how the database password is managed. |
| hub.minimumTokenLifetime | string | `jupyterhub.cull.maxAge` if lab culling is enabled, else none | Minimum remaining token lifetime when spawning a lab. The token cannot be renewed, so it should ideally live as long as the lab does. If the token has less remaining lifetime, the user will be redirected to reauthenticate before spawning a lab. |
| hub.resources | object | See `values.yaml` | Resource limits and requests for the Hub |
| hub.timeout.startup | int | `90` | Timeout for JupyterLab to start in seconds. Currently this sometimes takes over 60 seconds for reasons we don't understand. |
| jupyterhub.cull.enabled | bool | `true` | Enable the lab culler. |
| jupyterhub.cull.every | int | 300 (5 minutes) | How frequently to check for idle labs in seconds |
| jupyterhub.cull.maxAge | int | 2160000 (25 days) | Maximum age of a lab regardless of activity |
| jupyterhub.cull.removeNamedServers | bool | `true` | Whether to remove named servers when culling their lab |
| jupyterhub.cull.timeout | int | 432000 (5 days) | Default idle timeout before the lab is automatically deleted in seconds |
| jupyterhub.cull.users | bool | `false` | Whether to log out the user (from JupyterHub) when culling their lab |
| jupyterhub.hub.authenticatePrometheus | bool | `false` | Whether to require metrics requests to be authenticated |
| jupyterhub.hub.baseUrl | string | `"/nb"` | Base URL on which JupyterHub listens |
| jupyterhub.hub.containerSecurityContext | object | See `values.yaml` | Security context for JupyterHub container |
| jupyterhub.hub.db.password | string | Comes from nublado-secret | Database password (not used) |
| jupyterhub.hub.db.type | string | `"postgres"` | Type of database to use |
| jupyterhub.hub.db.upgrade | bool | `false` | Whether to automatically update DB schema at Hub start |
| jupyterhub.hub.db.url | string | Use the in-cluster PostgreSQL installed by Phalanx | URL of PostgreSQL server |
| jupyterhub.hub.existingSecret | string | `"nublado-secret"` | Existing secret to use for private keys |
| jupyterhub.hub.extraEnv | object | Gets `JUPYTERHUB_CRYPT_KEY` from `nublado-secret` | Additional environment variables to set |
| jupyterhub.hub.extraVolumeMounts | list | `hub-config` and the Gafaelfawr token | Additional volume mounts for JupyterHub |
| jupyterhub.hub.extraVolumes | list | The `hub-config` `ConfigMap` and the Gafaelfawr token | Additional volumes to make available to JupyterHub |
| jupyterhub.hub.image.name | string | `"ghcr.io/lsst-sqre/nublado-jupyterhub"` | Image to use for JupyterHub |
| jupyterhub.hub.image.tag | string | `"8.4.1"` | Tag of image to use for JupyterHub |
| jupyterhub.hub.loadRoles.server.scopes | list | `["self"]` | Default scopes for the user's lab, overridden to allow the lab to delete itself (which we use for our added menu items) |
| jupyterhub.hub.networkPolicy.enabled | bool | `false` | Whether to enable the default `NetworkPolicy` (currently, the upstream one does not work correctly) |
| jupyterhub.hub.resources | object | See `values.yaml` | Resource limits and requests |
| jupyterhub.ingress.enabled | bool | `false` | Whether to enable the default ingress. Should always be disabled since we install our own `GafaelfawrIngress` to avoid repeating the global hostname and manually configuring authentication |
| jupyterhub.prePuller.continuous.enabled | bool | `false` | Whether to run the JupyterHub continuous prepuller (the Nublado controller does its own prepulling) |
| jupyterhub.prePuller.hook.enabled | bool | `false` | Whether to run the JupyterHub hook prepuller (the Nublado controller does its own prepulling) |
| jupyterhub.proxy.chp.networkPolicy.interNamespaceAccessLabels | string | `"accept"` | Enable access to the proxy from other namespaces, since we put each user's lab environment in its own namespace |
| jupyterhub.proxy.chp.resources | object | See `values.yaml` | Resource limits and requests for proxy pod |
| jupyterhub.proxy.service.type | string | `"ClusterIP"` | Only expose the proxy to the cluster, overriding the default of exposing the proxy directly to the Internet |
| jupyterhub.scheduling.userPlaceholder.enabled | bool | `false` | Whether to spawn placeholder pods representing fake users to force autoscaling in advance of running out of resources |
| jupyterhub.scheduling.userScheduler.enabled | bool | `false` | Whether the user scheduler should be enabled |
| proxy.ingress.annotations | object | See `values.yaml` | Additional annotations to add to the proxy ingress (also used to talk to JupyterHub and all user labs) |
| secrets.templateSecrets | bool | `true` | Whether to use the new secrets management mechanism. If enabled, the Vault nublado secret will be split into a nublado secret for JupyterHub and a nublado-lab-secret secret used as a source for secret values for the user's lab. |
