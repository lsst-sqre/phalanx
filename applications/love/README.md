# love

Deployment for the LSST Operators Visualization Environment

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.controlSystem.appNamespace | string | Set by ArgoCD | Application namespace for the control system deployment |
| global.controlSystem.imageTag | string | Set by ArgoCD | Image tag for the control system deployment |
| global.controlSystem.kafkaBrokerAddress | string | Set by ArgoCD | Kafka broker address for the control system deployment |
| global.controlSystem.kafkaTopicReplicationFactor | string | Set by ArgoCD | Kafka topic replication factor for control system topics |
| global.controlSystem.s3EndpointUrl | string | Set by ArgoCD | S3 endpoint (LFA) for the control system deployment |
| global.controlSystem.schemaRegistryUrl | string | Set by ArgoCD | Schema registry URL for the control system deployment |
| global.controlSystem.siteTag | string | Set by ArgoCD | Site tag for the control system deployment |
| global.controlSystem.topicName | string | Set by ArgoCD | Topic name tag for the control system deployment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| csc_collector.secrets | list | `[]` | This section holds secret specifications. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the secret) _key_ (The key in the vault store where the secret resides) _type_ (OPTIONAL: The secret type. Defaults to Opaque.) |
| love-manager.envSecretKeyName | string | `"love"` | The top-level secret key name that houses the rest of the secrets |
| love-manager.manager.frontend.affinity | object | `{}` | Affinity rules for the LOVE manager frontend pods |
| love-manager.manager.frontend.autoscaling.enabled | bool | `true` | Whether automatic horizontal scaling is active |
| love-manager.manager.frontend.autoscaling.maxReplicas | int | `100` | The allowed maximum number of replicas |
| love-manager.manager.frontend.autoscaling.minReplicas | int | `1` | The allowed minimum number of replicas |
| love-manager.manager.frontend.autoscaling.scaleDownPolicy | object | `{}` | Policy for scaling down manager pods |
| love-manager.manager.frontend.autoscaling.scaleUpPolicy | object | `{}` | Policy for scaling up manager pods |
| love-manager.manager.frontend.autoscaling.targetCPUUtilizationPercentage | int | `80` | The percentage of CPU utilization that will trigger the scaling |
| love-manager.manager.frontend.autoscaling.targetMemoryUtilizationPercentage | int | `""` | The percentage of memory utilization that will trigger the scaling |
| love-manager.manager.frontend.env.AUTH_LDAP_1_SERVER_URI | string | `"ldap://ipa1.lsst.local"` | Set the URI for the 1st LDAP server |
| love-manager.manager.frontend.env.AUTH_LDAP_2_SERVER_URI | string | `"ldap://ipa2.lsst.local"` | Set the URI for the 2nd LDAP server |
| love-manager.manager.frontend.env.AUTH_LDAP_3_SERVER_URI | string | `"ldap://ipa3.lsst.local"` | Set the URI for the 3rd LDAP server |
| love-manager.manager.frontend.env.COMMANDER_HOSTNAME | string | `"love-commander-service"` | Label for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| love-manager.manager.frontend.env.COMMANDER_PORT | int | `5000` | Port number for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| love-manager.manager.frontend.env.DB_ENGINE | string | `"postgresql"` | The type of database engine being used for the LOVE manager frontend |
| love-manager.manager.frontend.env.DB_HOST | string | `"love-manager-database-service"` | The name of the database service |
| love-manager.manager.frontend.env.DB_NAME | string | `"love"` | The name of the database being used for the LOVE manager frontend |
| love-manager.manager.frontend.env.DB_PORT | int | `5432` | The port for the database service |
| love-manager.manager.frontend.env.DB_USER | string | `"love"` | The database user needed for access from the LOVE manager frontend |
| love-manager.manager.frontend.env.JIRA_API_HOSTNAME | string | `"jira.lsstcorp.org"` | Set the hostname for the Jira instance |
| love-manager.manager.frontend.env.JIRA_PROJECT_ID | int | `14601` | Set the Jira project ID |
| love-manager.manager.frontend.env.LOVE_PRODUCER_WEBSOCKET_HOST | string | `"love-service/manager/ws/subscription"` | The URL path for the LOVE producer websocket host |
| love-manager.manager.frontend.env.LOVE_SITE | string | `"local"` | The site tag where LOVE is being run |
| love-manager.manager.frontend.env.OLE_API_HOSTNAME | string | `"site.lsst.local"` | Set the URL for the OLE instance |
| love-manager.manager.frontend.env.REDIS_CONFIG_CAPACITY | int | `5000` | The connection capacity for the redis service |
| love-manager.manager.frontend.env.REDIS_CONFIG_EXPIRY | int | `5` | The expiration time for the redis service |
| love-manager.manager.frontend.env.REDIS_HOST | string | `"love-manager-redis-service"` | The name of the redis service |
| love-manager.manager.frontend.env.REMOTE_STORAGE | bool | `true` | Set the manager to use LFA storage |
| love-manager.manager.frontend.env.SERVER_URL | string | `"love.lsst.local"` | The external URL from the NGINX server for LOVE |
| love-manager.manager.frontend.env.URL_SUBPATH | string | `"/love"` | The Kubernetes sub-path for LOVE |
| love-manager.manager.frontend.envSecrets.ADMIN_USER_PASS | string | `"admin-user-pass"` | The LOVE manager frontend admin user password secret key name |
| love-manager.manager.frontend.envSecrets.AUTHLIST_USER_PASS | string | `"authlist-user-pass"` | The LOVE manager frontend authlist_user password secret key name |
| love-manager.manager.frontend.envSecrets.AUTH_LDAP_BIND_PASSWORD | string | `"auth-ldap-bind-password"` | The LOVE manager frontend LDAP binding password secret key name |
| love-manager.manager.frontend.envSecrets.CMD_USER_PASS | string | `"cmd-user-pass"` | The LOVE manager frontend cmd_user user password secret key name |
| love-manager.manager.frontend.envSecrets.DB_PASS | string | `"db-pass"` | The database password secret key name. Must match `database.envSecrets.POSTGRES_PASSWORD` |
| love-manager.manager.frontend.envSecrets.PROCESS_CONNECTION_PASS | string | `"process-connection-pass"` | The LOVE manager frontend process connection password secret key name |
| love-manager.manager.frontend.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name. Must match `redis.envSecrets.REDIS_PASS` |
| love-manager.manager.frontend.envSecrets.SECRET_KEY | string | `"manager-secret-key"` | The LOVE manager frontend secret secret key name |
| love-manager.manager.frontend.envSecrets.USER_USER_PASS | string | `"user-user-pass"` | The LOVE manager frontend user user password secret key name |
| love-manager.manager.frontend.image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| love-manager.manager.frontend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE manager frontend image |
| love-manager.manager.frontend.image.repository | string | `"lsstts/love-manager"` | The LOVE manager frontend image to use |
| love-manager.manager.frontend.nodeSelector | object | `{}` | Node selection rules for the LOVE manager frontend pods |
| love-manager.manager.frontend.ports.container | int | `8000` | The port on the container for normal communications |
| love-manager.manager.frontend.ports.node | int | `30000` | The port on the node for normal communcations |
| love-manager.manager.frontend.readinessProbe | object | `{}` | Configuration for the LOVE manager frontend pods readiness probe |
| love-manager.manager.frontend.replicas | int | `1` | Set the default number of LOVE manager frontend pod replicas |
| love-manager.manager.frontend.resources | object | `{}` | Resource specifications for the LOVE manager frontend pods |
| love-manager.manager.frontend.tolerations | list | `[]` | Toleration specifications for the LOVE manager frontend pods |
| love-manager.manager.producers.affinity | object | `{}` | Affinity rules for the LOVE manager producers pods |
| love-manager.manager.producers.autoscaling.enabled | bool | `true` | Whether automatic horizontal scaling is active |
| love-manager.manager.producers.autoscaling.maxReplicas | int | `100` | The allowed maximum number of replicas |
| love-manager.manager.producers.autoscaling.minReplicas | int | `1` | The allowed minimum number of replicas |
| love-manager.manager.producers.autoscaling.scaleDownPolicy | object | `{}` | Policy for scaling down manager pods |
| love-manager.manager.producers.autoscaling.scaleUpPolicy | object | `{}` | Policy for scaling up manager pods |
| love-manager.manager.producers.autoscaling.targetCPUUtilizationPercentage | int | `80` | The percentage of CPU utilization that will trigger the scaling |
| love-manager.manager.producers.autoscaling.targetMemoryUtilizationPercentage | int | `""` | The percentage of memory utilization that will trigger the scaling |
| love-manager.manager.producers.env.AUTH_LDAP_1_SERVER_URI | string | `"ldap://ipa1.lsst.local"` | Set the URI for the 1st LDAP server |
| love-manager.manager.producers.env.AUTH_LDAP_2_SERVER_URI | string | `"ldap://ipa2.lsst.local"` | Set the URI for the 2nd LDAP server |
| love-manager.manager.producers.env.AUTH_LDAP_3_SERVER_URI | string | `"ldap://ipa3.lsst.local"` | Set the URI for the 3rd LDAP server |
| love-manager.manager.producers.env.COMMANDER_HOSTNAME | string | `"love-commander-service"` | Label for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| love-manager.manager.producers.env.COMMANDER_PORT | int | `5000` | Port number for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| love-manager.manager.producers.env.DB_ENGINE | string | `"postgresql"` | The type of database engine being used for the LOVE manager producers |
| love-manager.manager.producers.env.DB_HOST | string | `"love-manager-database-service"` | The name of the database service |
| love-manager.manager.producers.env.DB_NAME | string | `"love"` | The name of the database being used for the LOVE manager producers |
| love-manager.manager.producers.env.DB_PORT | int | `5432` | The port for the database service |
| love-manager.manager.producers.env.DB_USER | string | `"love"` | The database user needed for access from the LOVE manager producers |
| love-manager.manager.producers.env.HEARTBEAT_QUERY_COMMANDER | bool | `false` | Have the LOVE producer managers not query commander |
| love-manager.manager.producers.env.JIRA_API_HOSTNAME | string | `"jira.lsstcorp.org"` | Set the hostname for the Jira instance |
| love-manager.manager.producers.env.JIRA_PROJECT_ID | int | `14601` | Set the Jira project ID |
| love-manager.manager.producers.env.LOVE_SITE | string | `"local"` | The site tag where LOVE is being run |
| love-manager.manager.producers.env.OLE_API_HOSTNAME | string | `"site.lsst.local"` | Set the URL for the OLE instance |
| love-manager.manager.producers.env.REDIS_CONFIG_CAPACITY | int | `5000` | The connection capacity for the redis service |
| love-manager.manager.producers.env.REDIS_CONFIG_EXPIRY | int | `5` | The expiration time for the redis service |
| love-manager.manager.producers.env.REDIS_HOST | string | `"love-manager-redis-service"` | The name of the redis service |
| love-manager.manager.producers.env.REMOTE_STORAGE | bool | `true` | Set the manager to use LFA storage |
| love-manager.manager.producers.env.SERVER_URL | string | `"love.lsst.local"` | The external URL from the NGINX server for LOVE |
| love-manager.manager.producers.env.URL_SUBPATH | string | `"/love"` | The Kubernetes sub-path for LOVE |
| love-manager.manager.producers.envSecrets.ADMIN_USER_PASS | string | `"admin-user-pass"` | The LOVE manager producers admin user password secret key name |
| love-manager.manager.producers.envSecrets.AUTHLIST_USER_PASS | string | `"authlist-user-pass"` | The LOVE manager producers authlist_user password secret key name |
| love-manager.manager.producers.envSecrets.AUTH_LDAP_BIND_PASSWORD | string | `"auth-ldap-bind-password"` | The LOVE manager producers LDAP binding password secret key name |
| love-manager.manager.producers.envSecrets.CMD_USER_PASS | string | `"cmd-user-pass"` | The LOVE manager producers cmd_user user password secret key name |
| love-manager.manager.producers.envSecrets.DB_PASS | string | `"db-pass"` | The database password secret key name. Must match `database.envSecrets.POSTGRES_PASSWORD` |
| love-manager.manager.producers.envSecrets.PROCESS_CONNECTION_PASS | string | `"process-connection-pass"` | The LOVE manager producers process connection password secret key name |
| love-manager.manager.producers.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name. Must match `redis.envSecrets.REDIS_PASS` |
| love-manager.manager.producers.envSecrets.SECRET_KEY | string | `"manager-secret-key"` | The LOVE manager producers secret secret key name |
| love-manager.manager.producers.envSecrets.USER_USER_PASS | string | `"user-user-pass"` | The LOVE manager producers user user password secret key name |
| love-manager.manager.producers.image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| love-manager.manager.producers.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE manager producers image |
| love-manager.manager.producers.image.repository | string | `"lsstts/love-manager"` | The LOVE manager producers image to use |
| love-manager.manager.producers.nodeSelector | object | `{}` | Node selection rules for the LOVE manager producers pods |
| love-manager.manager.producers.ports.container | int | `8000` | The port on the container for normal communications |
| love-manager.manager.producers.ports.node | int | `30000` | The port on the node for normal communcations |
| love-manager.manager.producers.readinessProbe | object | `{}` | Configuration for the LOVE manager producers pods readiness probe |
| love-manager.manager.producers.replicas | int | `1` | Set the default number of LOVE manager producers pod replicas |
| love-manager.manager.producers.resources | object | `{}` | Resource specifications for the LOVE manager producers pods |
| love-manager.manager.producers.tolerations | list | `[]` | Toleration specifications for the LOVE manager producers pods |
| love-manager.namespace | string | `"love"` | The overall namespace for the application |
| love-manager.redis.affinity | object | `{}` | Affinity rules for the LOVE redis pods |
| love-manager.redis.config | string | `"timeout 60\n"` | Configuration specification for the redis service |
| love-manager.redis.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name |
| love-manager.redis.image.pullPolicy | string | `"IfNotPresent"` | The pull policy for the redis image |
| love-manager.redis.image.repository | string | `"redis"` | The redis image to use |
| love-manager.redis.image.tag | string | `"7.2.4"` | The tag to use for the redis image |
| love-manager.redis.nodeSelector | object | `{}` | Node selection rules for the LOVE redis pods |
| love-manager.redis.port | int | `6379` | The redis port number |
| love-manager.redis.resources | object | `{}` | Resource specifications for the LOVE redis pods |
| love-manager.redis.tolerations | list | `[]` | Toleration specifications for the LOVE redis pods |
| love-manager.secret_path | string | `"lsst.local"` | The site-specific path to find Vault secrets |
| love-manager.viewBackup.affinity | object | `{}` | Affinity rules for the LOVE view backup pods |
| love-manager.viewBackup.enabled | bool | `false` | Whether view backup is active |
| love-manager.viewBackup.env | object | `{}` | Place to specify additional environment variables for the view backup job |
| love-manager.viewBackup.image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| love-manager.viewBackup.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the view backup image |
| love-manager.viewBackup.image.repository | string | `"lsstts/love-view-backup"` | The view backup image to use |
| love-manager.viewBackup.image.tag | string | `"develop"` | The tag to use for the view backup image |
| love-manager.viewBackup.nodeSelector | object | `{}` | Node selection rules for the LOVE view backup pods |
| love-manager.viewBackup.resources | object | `{}` | Resource specifications for the LOVE view backup pods |
| love-manager.viewBackup.restartPolicy | string | `"Never"` | The restart policy type for the view backup cronjob |
| love-manager.viewBackup.schedule | string | `"0 0 1 1 *"` | The view backup job schedule in cron format |
| love-manager.viewBackup.tolerations | list | `[]` | Toleration specifications for the LOVE view backup pods |
| love-manager.viewBackup.ttlSecondsAfterFinished | string | `""` | Time after view backup job finishes before deletion (ALPHA) |
| love-nginx.affinity | object | `{}` | Affinity rules for the NGINX pod |
| love-nginx.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the NGINX image |
| love-nginx.image.repository | string | `"nginx"` | The NGINX image to use |
| love-nginx.image.tag | string | `"1.25.3"` | The tag to use for the NGINX image |
| love-nginx.imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. If this section is used, each object listed can have the following attributes defined: _name_ (The label identifying the pull-secret to use) |
| love-nginx.ingress.annotations | object | `{}` | Annotations for the NGINX ingress |
| love-nginx.ingress.className | string | `"nginx"` | Assign the Ingress class name |
| love-nginx.ingress.hostname | string | `"love.local"` | Hostname for the NGINX ingress |
| love-nginx.ingress.httpPath | string | `"/"` | Path name associated with the NGINX ingress |
| love-nginx.ingress.pathType | string | `""` | Set the Kubernetes path type for the NGINX ingress |
| love-nginx.initContainers.frontend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the frontend image |
| love-nginx.initContainers.frontend.image.repository | string | `"lsstts/love-frontend"` | The frontend image to use |
| love-nginx.initContainers.frontend.image.tag | string | `nil` |  |
| love-nginx.initContainers.manager.command | list | `["/bin/sh","-c","mkdir -p /usr/src/love-manager/media/thumbnails; mkdir -p /usr/src/love-manager/media/configs; cp -Rv /usr/src/love/manager/static /usr/src/love-manager; cp -uv /usr/src/love/manager/ui_framework/fixtures/thumbnails/* /usr/src/love-manager/media/thumbnails; cp -uv /usr/src/love/manager/api/fixtures/configs/* /usr/src/love-manager/media/configs"]` | The command to execute for the love-manager static content |
| love-nginx.initContainers.manager.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the love-manager static content image |
| love-nginx.initContainers.manager.image.repository | string | `"lsstts/love-manager"` | The static love-manager content image to use |
| love-nginx.initContainers.manager.image.tag | string | `nil` |  |
| love-nginx.loveConfig | string | `"{\n  \"alarms\": {\n    \"minSeveritySound\": \"serious\",\n    \"minSeverityNotification\": \"warning\"\n  },\n  \"camFeeds\": {\n    \"generic\": \"/gencam\",\n    \"allSky\": \"/gencam\"\n  }\n}\n"` | Configuration specificiation for the LOVE service |
| love-nginx.namespace | string | `"love"` | The overall namespace for the application |
| love-nginx.nginxConfig | string | `"server {\n  listen 80;\n  server_name localhost;\n  location / {\n    root   /usr/src/love-frontend;\n    try_files $uri$args $uri$args/ $uri/ /index.html;\n  }\n  location /manager {\n      proxy_pass http://love-manager-service:8000;\n      proxy_http_version 1.1;\n      proxy_set_header Upgrade $http_upgrade;\n      proxy_set_header Connection \"upgrade\";\n      proxy_set_header Host $host;\n      proxy_redirect off;\n  }\n  location /manager/static {\n      alias /usr/src/love-manager/static;\n  }\n  location /manager/media {\n      alias /usr/src/love-manager/media;\n  }\n}\n"` | Configuration specification for the NGINX service |
| love-nginx.nodeSelector | object | `{}` | Node selection rules for the NGINX pod |
| love-nginx.ports.container | int | `80` | Container port for the NGINX service |
| love-nginx.ports.node | int | `30000` | Node port for the NGINX service |
| love-nginx.resources | object | `{}` | Resource specifications for the NGINX pod |
| love-nginx.serviceType | string | `"ClusterIP"` | Service type specification |
| love-nginx.staticStore.accessMode | string | `"ReadWriteMany"` | The access mode for the NGINX static store |
| love-nginx.staticStore.claimSize | string | `"2Gi"` | The size of the NGINX static store request |
| love-nginx.staticStore.name | string | `"love-nginx-static"` | Label for the NGINX static store |
| love-nginx.staticStore.storageClass | string | `"local-store"` | The storage class to request the disk allocation from |
| love-nginx.tolerations | list | `[]` | Toleration specifications for the NGINX pod |
| love-producer.affinity | object | `{}` | Affinity rules applied to all LOVE producer pods |
| love-producer.annotations | object | `{}` | This allows for the specification of pod annotations. |
| love-producer.env | object | `{"WEBSOCKET_HOST":"love-nginx/manager/ws/subscription"}` | This section holds a set of key, value pairs for environmental variables |
| love-producer.envSecrets | object | `{"PROCESS_CONNECTION_PASS":"process-connection-pass"}` | This section holds a set of key, value pairs for secrets |
| love-producer.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE producer image |
| love-producer.image.repository | string | `"lsstts/love-producer"` | The LOVE producer image to use |
| love-producer.image.tag | string | `nil` |  |
| love-producer.nodeSelector | object | `{}` | Node selection rules applied to all LOVE producer pods |
| love-producer.producers | obj | `[]` | This sections sets the list of producers to use. The producers should be specified like: _name_: The identifying name for the CSC producer _csc_: _CSC name:index_ The following attributes are optional _resources_ (A resource object specification) _nodeSelector_ (A node selector object specification) _tolerations_ (A list of tolerations) _affinity_ (An affinity object specification) |
| love-producer.replicaCount | int | `1` | Set the replica count for the LOVE producers |
| love-producer.resources | object | `{}` | Resource specifications applied to all LOVE producer pods |
| love-producer.tolerations | list | `[]` | Toleration specifications applied to all LOVE producer pods |
