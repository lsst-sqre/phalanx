# nublado

JupyterHub and custom spawner for the Rubin Science Platform

**Homepage:** <https://github.com/lsst-sqre/jupyterlab-controller>

## Source Code

* <https://github.com/lsst-sqre/jupyterlab-controller>
* <https://github.com/lsst-sqre/rsp-restspawner>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the nublado frontend pod |
| controller.images.docker.repository | string | `"library/sketchbook"` |  |
| controller.images.numDailies | int | `3` |  |
| controller.images.numReleases | int | `1` |  |
| controller.images.numWeeklies | int | `2` |  |
| controller.images.recommendedTag | string | `"recommended"` |  |
| controller.images.registry | string | `"lighthouse.ceres"` | config from sqr-066 |
| controller.lab | object | `{"env":{"API_ROUTE":"/api","AUTO_REPO_SPECS":"https://github.com/lsst-sqre/system-test@prod,https://github.com/rubin-dp0/tutorial-notebooks@prod","CULL_KERNEL_CONNECTED":"True","CULL_KERNEL_IDLE_TIMEOUT":"432000","CULL_KERNEL_INTERVAL":"300","DAF_BUTLER_REPOSITORY_INDEX":"s3://butler-us-central1-repo-locations/data-repos.yaml","FIREFLY_ROUTE":"/portal/app","HUB_ROUTE":"/nb/hub","JUPYTERHUB_ADMIN_ACCESS":"1","JUPYTERHUB_API_URL":"http://hub.nublado:8081/nb/hub/api","JUPYTERHUB_BASE_URL":"/nb/","JUPYTERHUB_DEFAULT_URL":"/lab","JUPYTERHUB_OAUTH_CLIENT_ALLOWED_SCOPES":"[]","NO_ACTIVITY_TIMEOUT":"432000","NO_SUDO":"TRUE","S3_ENDPOINT_URL":"https://storage.googleapis.com","SODA_ROUTE":"/api/image/soda","TAP_ROUTE":"/api/tap"},"files":{"/etc/group":{"contents":"root:x:0:\nbin:x:1:\ndaemon:x:2:\nsys:x:3:\nadm:x:4:\ntty:x:5:\ndisk:x:6:\nlp:x:7:\nmem:x:8:\nkmem:x:9:\nwheel:x:10:\ncdrom:x:11:\nmail:x:12:\nman:x:15:\ndialout:x:18:\nfloppy:x:19:\ngames:x:20:\nutmp:x:22:\ntape:x:33:\nutempter:x:35:\nvideo:x:39:\nftp:x:50:\nlock:x:54:\ntss:x:59:\naudio:x:63:\ndbus:x:81:\nscreen:x:84:\nnobody:x:99:\nusers:x:100:\nsystemd-journal:x:190:\nsystemd-network:x:192:\ncgred:x:997:\nssh_keys:x:998:\ninput:x:999:\n","modify":true},"/etc/passwd":{"contents":"root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\ntss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\nlsst_lcl:x:1000:1000::/home/lsst_lcl:/bin/bash\n","modify":true},"/opt/lsst/software/jupyterlab/lsst_dask.yml":{"contents":"# No longer used, but preserves compatibility with runlab.sh\ndask_worker.yml: |\n  enabled: false\n","modify":false},"/opt/lsst/software/jupyterlab/panda":{"contents":"# Licensed under the Apache License, Version 2.0 (the \"License\");\n# You may not use this file except in compliance with the License.\n# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0\n#\n# Authors:\n# - Wen Guan, <wen.guan@cern.ch>, 2020\n[common]\n# if logdir is configured, idds will write to idds.log in this directory.\n# else idds will go to stdout/stderr.\n# With supervisord, it's good to write to stdout/stderr, then supervisord can manage and rotate logs.\n# logdir = /var/log/idds\nloglevel = INFO\n[rest]\nhost = https://iddsserver.cern.ch:443/idds\n#url_prefix = /idds\n#cacher_dir = /tmp\ncacher_dir = /data/idds\n","modify":false}},"initcontainers":[],"secrets":[],"sizes":{"large":{"cpu":4,"memory":"12Gi"},"medium":{"cpu":2,"memory":"6Gi"},"small":{"cpu":1,"memory":"3Gi"}},"volumes":[{"containerPath":"/home","mode":"rw","server":"10.13.105.122","serverPath":"/share1/home"},{"containerPath":"/project","mode":"ro","server":"10.13.105.122","serverPath":"/share1/project"},{"containerPath":"/scratch","mode":"rw","server":"10.13.105.122","serverPath":"/share1/scratch"}]}` | Settings for the JupyterLab controller |
| controller.lab.env | object | `{"API_ROUTE":"/api","AUTO_REPO_SPECS":"https://github.com/lsst-sqre/system-test@prod,https://github.com/rubin-dp0/tutorial-notebooks@prod","CULL_KERNEL_CONNECTED":"True","CULL_KERNEL_IDLE_TIMEOUT":"432000","CULL_KERNEL_INTERVAL":"300","DAF_BUTLER_REPOSITORY_INDEX":"s3://butler-us-central1-repo-locations/data-repos.yaml","FIREFLY_ROUTE":"/portal/app","HUB_ROUTE":"/nb/hub","JUPYTERHUB_ADMIN_ACCESS":"1","JUPYTERHUB_API_URL":"http://hub.nublado:8081/nb/hub/api","JUPYTERHUB_BASE_URL":"/nb/","JUPYTERHUB_DEFAULT_URL":"/lab","JUPYTERHUB_OAUTH_CLIENT_ALLOWED_SCOPES":"[]","NO_ACTIVITY_TIMEOUT":"432000","NO_SUDO":"TRUE","S3_ENDPOINT_URL":"https://storage.googleapis.com","SODA_ROUTE":"/api/image/soda","TAP_ROUTE":"/api/tap"}` | Environment variables for user lab pods, common to all lab pods in this RSP instance. |
| controller.lab.files | object | `{"/etc/group":{"contents":"root:x:0:\nbin:x:1:\ndaemon:x:2:\nsys:x:3:\nadm:x:4:\ntty:x:5:\ndisk:x:6:\nlp:x:7:\nmem:x:8:\nkmem:x:9:\nwheel:x:10:\ncdrom:x:11:\nmail:x:12:\nman:x:15:\ndialout:x:18:\nfloppy:x:19:\ngames:x:20:\nutmp:x:22:\ntape:x:33:\nutempter:x:35:\nvideo:x:39:\nftp:x:50:\nlock:x:54:\ntss:x:59:\naudio:x:63:\ndbus:x:81:\nscreen:x:84:\nnobody:x:99:\nusers:x:100:\nsystemd-journal:x:190:\nsystemd-network:x:192:\ncgred:x:997:\nssh_keys:x:998:\ninput:x:999:\n","modify":true},"/etc/passwd":{"contents":"root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\ntss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\nlsst_lcl:x:1000:1000::/home/lsst_lcl:/bin/bash\n","modify":true},"/opt/lsst/software/jupyterlab/lsst_dask.yml":{"contents":"# No longer used, but preserves compatibility with runlab.sh\ndask_worker.yml: |\n  enabled: false\n","modify":false},"/opt/lsst/software/jupyterlab/panda":{"contents":"# Licensed under the Apache License, Version 2.0 (the \"License\");\n# You may not use this file except in compliance with the License.\n# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0\n#\n# Authors:\n# - Wen Guan, <wen.guan@cern.ch>, 2020\n[common]\n# if logdir is configured, idds will write to idds.log in this directory.\n# else idds will go to stdout/stderr.\n# With supervisord, it's good to write to stdout/stderr, then supervisord can manage and rotate logs.\n# logdir = /var/log/idds\nloglevel = INFO\n[rest]\nhost = https://iddsserver.cern.ch:443/idds\n#url_prefix = /idds\n#cacher_dir = /tmp\ncacher_dir = /data/idds\n","modify":false}}` | Files to be mounted as ConfigMaps inside the user lab pod. Some of these will require modification.  Those are noted with modify: true, and the file name will be the unique key directing how the Lab controller is to modify it. |
| controller.lab.initcontainers | list | `[]` | List of specifications for containers to run to commission a new user. |
| controller.lab.volumes | list | `[{"containerPath":"/home","mode":"rw","server":"10.13.105.122","serverPath":"/share1/home"},{"containerPath":"/project","mode":"ro","server":"10.13.105.122","serverPath":"/share1/project"},{"containerPath":"/scratch","mode":"rw","server":"10.13.105.122","serverPath":"/share1/scratch"}]` | Volumes defined to user lab pods |
| controller.runtime | object | `{"instanceUrl":"","namespace":"","path":""}` | Runtime config will be filled in on initialization |
| controller.safir | object | `{"logLevel":"DEBUG","loggerName":"jupyterlabcontroller","name":"jupyterlab-controller","profile":"development","rootEndpoint":"nublado"}` | safir settings; generically set through environment variables, but we'd rather do it this way and just control all config through the ConfigMap |
| controller.safir.loggerName | string | `"jupyterlabcontroller"` | Root name of the application's logger. |
| controller.safir.name | string | `"jupyterlab-controller"` | The application's name (not necessarily the root HTTP endpoint path) |
| controller.safir.profile | string | `"development"` | Application run profile: "development" or "production" |
| controller.safir.rootEndpoint | string | `"nublado"` | The application's root HTTP endpoint path |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the nublado image |
| image.repository | string | `"lsstsqre/jupyterlabcontroller"` | nublado image to use |
| image.tag | string | The appVersion of the chart | Tag of nublado image to use |
| ingress.annotations | object | `{}` | Additional annotations to add for endpoints that are authenticated. |
| jupyterhub.cull.enabled | bool | `true` |  |
| jupyterhub.cull.every | int | `600` |  |
| jupyterhub.cull.maxAge | int | `5184000` |  |
| jupyterhub.cull.removeNamedServers | bool | `true` |  |
| jupyterhub.cull.timeout | int | `2592000` |  |
| jupyterhub.cull.users | bool | `true` |  |
| jupyterhub.hub.authenticatePrometheus | bool | `false` |  |
| jupyterhub.hub.baseUrl | string | `"/nb"` |  |
| jupyterhub.hub.config.Authenticator.enable_auth_state | bool | `true` |  |
| jupyterhub.hub.config.JupyterHub.authenticator_class | string | `"rsp_restspawner.auth.GafaelfawrAuthenticator"` |  |
| jupyterhub.hub.config.JupyterHub.spawner_class | string | `"rsp_restspawner.RSPRestSpawner"` |  |
| jupyterhub.hub.config.ServerApp.shutdown_no_activity_timeout | int | `604800` |  |
| jupyterhub.hub.containerSecurityContext.allowPrivilegeEscalation | bool | `false` |  |
| jupyterhub.hub.containerSecurityContext.runAsGroup | int | `768` |  |
| jupyterhub.hub.containerSecurityContext.runAsUser | int | `768` |  |
| jupyterhub.hub.db.password | string | `"true"` |  |
| jupyterhub.hub.db.type | string | `"postgres"` |  |
| jupyterhub.hub.db.url | string | `"postgresql://jovyan@postgres.postgres/jupyterhub"` |  |
| jupyterhub.hub.existingSecret | string | `"nublado-secret"` |  |
| jupyterhub.hub.extraFiles."00_hub_config.py".mountPath | string | `"/usr/local/etc/jupyterhub/jupyterhub_config.d/00_hub_config.py"` |  |
| jupyterhub.hub.extraFiles."00_hub_config.py".stringData | string | `"import os\nimport rsp_restspawner  # Baked into image\nfrom rsp_restspawner.util import get_namespace\n\n# Turn off concurrent spawn limit\nc.JupyterHub.concurrent_spawn_limit = 0\n#\nc.JupyterHub.hub_connect_url = (\n    \"http://hub.\" +\n    f\"{get_namespace()}:\" +\n    f\"{os.environ['HUB_SERVICE_PORT']}\"\n)\n# Turn off restart after n consecutive failures\nc.Spawner.consecutive_failure_limit = 0\n# Use JupyterLab by default\nc.Spawner.default_url = \"/lab\"\nc.Spawner.start_timeout = 10 * 60  # 10 minutes\nc.Spawner.http_timeout = 90  # For debug mode and slow disks\n"` |  |
| jupyterhub.hub.extraVolumeMounts[0].mountPath | string | `"/etc/jupyterhub/nublado_config.yaml"` |  |
| jupyterhub.hub.extraVolumeMounts[0].name | string | `"nublado-config"` |  |
| jupyterhub.hub.extraVolumeMounts[0].subPath | string | `"nublado_config.yaml"` |  |
| jupyterhub.hub.extraVolumeMounts[1].mountPath | string | `"/etc/secret/admin-token"` |  |
| jupyterhub.hub.extraVolumeMounts[1].name | string | `"nublado-gafaelfawr"` |  |
| jupyterhub.hub.extraVolumeMounts[1].subPath | string | `"token"` |  |
| jupyterhub.hub.extraVolumes[0].configMap.name | string | `"nublado-config"` |  |
| jupyterhub.hub.extraVolumes[0].name | string | `"nublado-config"` |  |
| jupyterhub.hub.extraVolumes[1].name | string | `"nublado-gafaelfawr"` |  |
| jupyterhub.hub.extraVolumes[1].secret.secretName | string | `"gafaelfawr-token"` |  |
| jupyterhub.hub.image.name | string | `"docker.io/lsstsqre/rsp-restspawner"` |  |
| jupyterhub.hub.loadRoles.self.scopes[0] | string | `"admin:servers!user"` |  |
| jupyterhub.hub.loadRoles.self.scopes[1] | string | `"read:metrics"` |  |
| jupyterhub.hub.loadRoles.server.scopes[0] | string | `"inherit"` |  |
| jupyterhub.hub.networkPolicy.enabled | bool | `false` |  |
| jupyterhub.hub.resources.limits.cpu | string | `"900m"` |  |
| jupyterhub.hub.resources.limits.memory | string | `"1Gi"` |  |
| jupyterhub.imagePullSecrets[0].name | string | `"pull-secret"` |  |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/auth-method" | string | `"GET"` |  |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/auth-response-headers" | string | `"X-Auth-Request-Token"` |  |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/auth-url" | string | `"http://gafaelfawr.gafaelfawr.svc.cluster.local:8080/auth?scope=exec:notebook&notebook=true&minimum_lifetime=2160000"` |  |
| jupyterhub.ingress.annotations."nginx.ingress.kubernetes.io/configuration-snippet" | string | `"error_page 403 = \"/auth/forbidden?scope=exec:notebook\";\n"` |  |
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
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the nublado frontend pod |
| podAnnotations | object | `{}` | Annotations for the nublado frontend pod |
| resources | object | `{}` | Resource limits and requests for the nublado frontend pod |
| serviceAccount | object | `{"annotations":{},"name":""}` | Secret names to use for all Docker pulls |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.name | string | Name based on the fullname template | Name of the service account to use |
| tolerations | list | `[]` | Tolerations for the nublado frontend pod |
