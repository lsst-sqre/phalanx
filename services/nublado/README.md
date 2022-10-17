# nublado

Service to manage user labs

**Homepage:** <https://github.com/lsst-sqre/jupyterlab-controller>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the nublado frontend pod |
| controller.lab | object | `{"env":{"AUTO_REPO_BRANCH":"prod","AUTO_REPO_SPECS":"https://github.com/lsst-sqre/system-test@prod,https://github.com/rubin-dp0/tutorial-notebooks@prod","AUTO_REPO_URLS":"https://github.com/lsst-sqre/system-test,https://github.com/rubin-dp0/tutorial-notebooks","AWS_SHARED_CREDENTIALS_FILE":"/opt/lsst/software/jupyterlab/butler-secret/aws-credentials.ini","BASE_URL":"{{ Values.config.base_url }}","CULL_KERNEL_CONNECTED":"True","CULL_KERNEL_IDLE_TIMEOUT":"432000","CULL_KERNEL_INTERVAL":"300","DAF_BUTLER_REPOSITORY_INDEX":"s3://butler-us-central1-repo-locations/data-repos.yaml","GOOGLE_APPLICATION_CREDENTIALS":"/opt/lsst/software/jupyterlab/butler-secret/butler-gcs-idf-creds.json","NO_ACTIVITY_TIMEOUT":"432000","PGPASSFILE":"/opt/lsst/software/jupyterlab/butler-secret/postgres-credentials.txt","S3_ENDPOINT_URL":"https://storage.googleapis.com"},"files":{"group":"root:x:0:\nbin:x:1:\ndaemon:x:2:\nsys:x:3:\nadm:x:4:\ntty:x:5:\ndisk:x:6:\nlp:x:7:\nmem:x:8:\nkmem:x:9:\nwheel:x:10:\ncdrom:x:11:\nmail:x:12:\nman:x:15:\ndialout:x:18:\nfloppy:x:19:\ngames:x:20:\nutmp:x:22:\ntape:x:33:\nutempter:x:35:\nvideo:x:39:\nftp:x:50:\nlock:x:54:\ntss:x:59:\naudio:x:63:\ndbus:x:81:\nscreen:x:84:\nnobody:x:99:\nusers:x:100:\nsystemd-journal:x:190:\nsystemd-network:x:192:\ncgred:x:997:\nssh_keys:x:998:\ninput:x:999:\n","idds":"# Licensed under the Apache License, Version 2.0 (the \"License\");\n# You may not use this file except in compliance with the License.\n# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0\n#\n# Authors:\n# - Wen Guan, <wen.guan@cern.ch>, 2020\n[common]\n# if logdir is configured, idds will write to idds.log in this\n# directory, otherwise to to stdout/stderr.\n# With supervisord, it's good to write to stdout/stderr, then\n# supervisord can manage and rotate logs.\n# logdir = /var/log/idds\nloglevel = INFO\n[rest]\nhost = https://iddsserver.cern.ch:443/idds\n#url_prefix = /idds\n#cacher_dir = /tmp\ncacher_dir = /data/idds\n","passwd":"root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\ntss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\nlsst_lcl:x:1000:1000::/home/lsst_lcl:/bin/bash\n"},"quota":{"cpu":81,"memory":"243Gi"},"sizes":{"large":{"cpu":4,"memory":"12Gi"},"medium":{"cpu":2,"memory":"6Gi"},"small":{"cpu":1,"memory":"3Gi"}},"volume_mounts":[{"mountPath":"/home","name":"home"},{"mountPath":"/project","name":"project"},{"mountPath":"/scratch","name":"scratch"}],"volumes":[{"name":"home","nfs":{"path":"/share1/home","server":"10.13.105.122"}},{"name":"project","nfs":{"path":"/share1/project","server":"10.13.105.122"}},{"name":"scratch","nfs":{"path":"/share1/scratch","server":"10.13.105.122"}}]}` | Settings for the JupyterLab controller |
| controller.lab.quota | object | `{"cpu":81,"memory":"243Gi"}` | Maximum CPU/memory resources for user namespace |
| controller.lab.volume_mounts | list | `[{"mountPath":"/home","name":"home"},{"mountPath":"/project","name":"project"},{"mountPath":"/scratch","name":"scratch"}]` | Volume Mounts corresponding to user lab pod Volumes |
| controller.lab.volumes | list | `[{"name":"home","nfs":{"path":"/share1/home","server":"10.13.105.122"}},{"name":"project","nfs":{"path":"/share1/project","server":"10.13.105.122"}},{"name":"scratch","nfs":{"path":"/share1/scratch","server":"10.13.105.122"}}]` | Volumes defined to user lab pods |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the nublado image |
| image.repository | string | `"lsstsqre/nublado"` | nublado image to use |
| image.tag | string | The appVersion of the chart | Tag of nublado image to use |
| ingress.annotations | object | `{}` | Additional annotations to add for endpoints that are authenticated. |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the nublado frontend pod |
| podAnnotations | object | `{}` | Annotations for the nublado frontend pod |
| resources | object | `{}` | Resource limits and requests for the nublado frontend pod |
| serviceAccount | object | `{"annotations":{},"name":""}` | Secret names to use for all Docker pulls |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.name | string | Name based on the fullname template | Name of the service account to use |
| tolerations | list | `[]` | Tolerations for the nublado frontend pod |
