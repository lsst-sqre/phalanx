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
| audio-broadcaster.affinity | object | `{}` | Affinity rules for the ts_audio_broadcaster pods |
| audio-broadcaster.env | object | `{"WEBSERVER_PORT":8888}` | This section holds a set of key, value pairs for environmental variables |
| audio-broadcaster.fullnameOverride | string | `""` | Specify the deployed application name specifically. Overrides all other names. |
| audio-broadcaster.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the ts_audio_broadcaster image |
| audio-broadcaster.image.repository | string | `"lsstts/audio_broadcaster"` | The ts_audio_broadcaster image to use |
| audio-broadcaster.image.revision | int | `nil` | The cycle revision to add to the image tag |
| audio-broadcaster.ingress.annotations | object | `{}` | Annotations for the ts_audio_broadcaster ingress |
| audio-broadcaster.ingress.className | string | `"nginx"` | Assign the Ingress class name |
| audio-broadcaster.ingress.hostname | string | `"audio-broadcaster.local"` | Hostname for the ts_audio_broadcaster ingress |
| audio-broadcaster.ingress.httpPath | string | `"/"` | Path name associated with the ts_audio_broadcaster ingress |
| audio-broadcaster.ingress.pathType | string | `"Exact"` | Set the Kubernetes path type for the ts_audio_broadcaster ingress |
| audio-broadcaster.microphones | list | `[]` | This sections sets the list of producers to use. The microphones should be specified like: _name_: _host_: _Microphone host_ _port_: _Microphone port_ Example: auxtel1: host: localhost port: 4444 |
| audio-broadcaster.nameOverride | string | `""` | Adds an extra string to the release name. |
| audio-broadcaster.namespace | string | `"love"` | The overall namespace for the ts_audio_broadcaster |
| audio-broadcaster.nodeSelector | object | `{}` | Node selection rules for the ts_audio_broadcaster pods |
| audio-broadcaster.podAnnotations | object | `{}` | This allows the specification of pod annotations. |
| audio-broadcaster.ports.container | int | `80` | Container port for the ts_audio_broadcaster service |
| audio-broadcaster.ports.node | int | `30000` | Node port for the ts_audio_broadcaster service |
| audio-broadcaster.replicaCount | int | `1` | Set the replica count for the ts_audio_broadcasters |
| audio-broadcaster.resources | object | `{}` | Resource specifications for the ts_audio_broadcaster pods |
| audio-broadcaster.serviceType | string | `"ClusterIP"` | Service type specification |
| audio-broadcaster.tolerations | list | `[]` | Toleration specifications for the ts_audio_broadcaster pods |
| love-manager.manager | object | `{"frontend":{"affinity":{},"autoscaling":{"enabled":true,"maxReplicas":100,"minReplicas":1,"scaleDownPolicy":{},"scaleUpPolicy":{},"targetCPUUtilizationPercentage":80,"targetMemoryUtilizationPercentage":""},"env":{"AUTH_LDAP_1_SERVER_URI":"ldap://ipa1.lsst.local","AUTH_LDAP_2_SERVER_URI":"ldap://ipa2.lsst.local","AUTH_LDAP_3_SERVER_URI":"ldap://ipa3.lsst.local","COMMANDER_HOSTNAME":"love-commander-service","COMMANDER_PORT":5000,"DB_ENGINE":"postgresql","DB_HOST":"love-manager-database-service","DB_NAME":"love","DB_PORT":5432,"DB_USER":"love","JIRA_API_HOSTNAME":"rubinobs.atlassian.net","JIRA_PROJECT_ID":10063,"LOVE_PRODUCER_WEBSOCKET_HOST":"love-service/manager/ws/subscription","LOVE_SITE":"local","NIGHTREPORT_MAIL_ADDRESS":"rubin-night-log@lists.lsst.org","OLE_API_HOSTNAME":"site.lsst.local","REDIS_CONFIG_CAPACITY":5000,"REDIS_CONFIG_EXPIRY":5,"REDIS_HOST":"love-manager-redis-service","REMOTE_STORAGE":true,"SERVER_URL":"love.lsst.local","SMTP_USER":"loveapplication","URL_SUBPATH":"/love"},"envSecrets":{"ADMIN_USER_PASS":"admin-user-pass","AUTHLIST_USER_PASS":"authlist-user-pass","AUTH_LDAP_BIND_PASSWORD":"auth-ldap-bind-password","CMD_USER_PASS":"cmd-user-pass","DB_PASS":"db-pass","JIRA_API_TOKEN":"jira-api-token","PROCESS_CONNECTION_PASS":"process-connection-pass","REDIS_PASS":"redis-pass","SECRET_KEY":"manager-secret-key","SMTP_PASSWORD":"smtp-email-password","USER_USER_PASS":"user-user-pass"},"image":{"nexus3":"","pullPolicy":"IfNotPresent","repository":"lsstts/love-manager","revision":null},"nodeSelector":{},"ports":{"container":8000,"node":30000},"readinessProbe":{},"replicas":1,"resources":{},"tolerations":[]},"producers":[{"affinity":{},"autoscaling":{"enabled":true,"maxReplicas":100,"minReplicas":1,"scaleDownPolicy":{},"scaleUpPolicy":{},"targetCPUUtilizationPercentage":80,"targetMemoryUtilizationPercentage":""},"env":{"AUTH_LDAP_1_SERVER_URI":"ldap://ipa1.lsst.local","AUTH_LDAP_2_SERVER_URI":"ldap://ipa2.lsst.local","AUTH_LDAP_3_SERVER_URI":"ldap://ipa3.lsst.local","COMMANDER_HOSTNAME":"love-commander-service","COMMANDER_PORT":5000,"DB_ENGINE":"postgresql","DB_HOST":"love-manager-database-service","DB_NAME":"love","DB_PORT":5432,"DB_USER":"love","HEARTBEAT_QUERY_COMMANDER":false,"JIRA_API_HOSTNAME":"rubinobs.atlassian.net","JIRA_PROJECT_ID":10063,"LOVE_SITE":"local","OLE_API_HOSTNAME":"site.lsst.local","REDIS_CONFIG_CAPACITY":5000,"REDIS_CONFIG_EXPIRY":5,"REDIS_HOST":"love-manager-redis-service","REMOTE_STORAGE":true,"SERVER_URL":"love.lsst.local","URL_SUBPATH":"/love"},"envSecrets":{"ADMIN_USER_PASS":"admin-user-pass","AUTHLIST_USER_PASS":"authlist-user-pass","AUTH_LDAP_BIND_PASSWORD":"auth-ldap-bind-password","CMD_USER_PASS":"cmd-user-pass","DB_PASS":"db-pass","JIRA_API_TOKEN":"jira-api-token","PROCESS_CONNECTION_PASS":"process-connection-pass","REDIS_PASS":"redis-pass","SECRET_KEY":"manager-secret-key","USER_USER_PASS":"user-user-pass"},"image":{"nexus3":"","pullPolicy":"IfNotPresent","repository":"lsstts/love-manager","revision":null},"name":"example-producer","nodeSelector":{},"ports":{"container":8000,"node":30000},"readinessProbe":{},"replicas":1,"resources":{},"tolerations":[]}],"producers_ports":{"container":8000,"node":30000}}` | Configuration for the different manager instances. This is divided into two sessions; frontend and producers. _frontend_ Configuration for the manager frontend. The frontend session defines the configuration for the so-called frontend managers. These serves the frontend artifacts as well as handles the data piping from the system to the frontend. Every time a user opens a view in LOVE the page will connect to the frontend manager and will receive the telemetry data from the system. Once a connection is established between a frontend and the manager it is kept alive. As more connections come in, the autoscaler will scale up the number of frontend managers and new connections should be redirected to them. The redirect is handled by the manager-frontend-service ClusterIP. _producers_ Configurations for the manger producers. This is basically a list of managers (with the same structure as the frontend, but in a list). These defines services that the LOVE-producers connect to, to feed data from the control system. |
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
| love-manager.manager.frontend.env.JIRA_API_HOSTNAME | string | `"rubinobs.atlassian.net"` | Set the hostname for the Jira instance |
| love-manager.manager.frontend.env.JIRA_PROJECT_ID | int | `10063` | Set the Jira project ID |
| love-manager.manager.frontend.env.LOVE_PRODUCER_WEBSOCKET_HOST | string | `"love-service/manager/ws/subscription"` | The URL path for the LOVE producer websocket host |
| love-manager.manager.frontend.env.LOVE_SITE | string | `"local"` | The site tag where LOVE is being run |
| love-manager.manager.frontend.env.NIGHTREPORT_MAIL_ADDRESS | string | `"rubin-night-log@lists.lsst.org"` | The mail address to forward the nightly report to |
| love-manager.manager.frontend.env.OLE_API_HOSTNAME | string | `"site.lsst.local"` | Set the URL for the OLE instance |
| love-manager.manager.frontend.env.REDIS_CONFIG_CAPACITY | int | `5000` | The connection capacity for the redis service |
| love-manager.manager.frontend.env.REDIS_CONFIG_EXPIRY | int | `5` | The expiration time for the redis service |
| love-manager.manager.frontend.env.REDIS_HOST | string | `"love-manager-redis-service"` | The name of the redis service |
| love-manager.manager.frontend.env.REMOTE_STORAGE | bool | `true` | Set the manager to use LFA storage |
| love-manager.manager.frontend.env.SERVER_URL | string | `"love.lsst.local"` | The external URL from the NGINX server for LOVE |
| love-manager.manager.frontend.env.SMTP_USER | string | `"loveapplication"` | The SMTP user for the LOVE manager frontend |
| love-manager.manager.frontend.env.URL_SUBPATH | string | `"/love"` | The Kubernetes sub-path for LOVE |
| love-manager.manager.frontend.envSecrets.ADMIN_USER_PASS | string | `"admin-user-pass"` | The LOVE manager frontend admin user password secret key name |
| love-manager.manager.frontend.envSecrets.AUTHLIST_USER_PASS | string | `"authlist-user-pass"` | The LOVE manager frontend authlist_user password secret key name |
| love-manager.manager.frontend.envSecrets.AUTH_LDAP_BIND_PASSWORD | string | `"auth-ldap-bind-password"` | The LOVE manager frontend LDAP binding password secret key name |
| love-manager.manager.frontend.envSecrets.CMD_USER_PASS | string | `"cmd-user-pass"` | The LOVE manager frontend cmd_user user password secret key name |
| love-manager.manager.frontend.envSecrets.DB_PASS | string | `"db-pass"` | The database password secret key name. Must match `database.envSecrets.POSTGRES_PASSWORD` |
| love-manager.manager.frontend.envSecrets.JIRA_API_TOKEN | string | `"jira-api-token"` | The LOVE manager jira API token secret key name |
| love-manager.manager.frontend.envSecrets.PROCESS_CONNECTION_PASS | string | `"process-connection-pass"` | The LOVE manager frontend process connection password secret key name |
| love-manager.manager.frontend.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name. Must match `redis.envSecrets.REDIS_PASS` |
| love-manager.manager.frontend.envSecrets.SECRET_KEY | string | `"manager-secret-key"` | The LOVE manager frontend secret secret key name |
| love-manager.manager.frontend.envSecrets.SMTP_PASSWORD | string | `"smtp-email-password"` | The LOVE manager smtp email password secret key name |
| love-manager.manager.frontend.envSecrets.USER_USER_PASS | string | `"user-user-pass"` | The LOVE manager frontend user user password secret key name |
| love-manager.manager.frontend.image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| love-manager.manager.frontend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE manager frontend image |
| love-manager.manager.frontend.image.repository | string | `"lsstts/love-manager"` | The LOVE manager frontend image to use |
| love-manager.manager.frontend.image.revision | int | `nil` | The cycle revision to add to the image tag |
| love-manager.manager.frontend.nodeSelector | object | `{}` | Node selection rules for the LOVE manager frontend pods |
| love-manager.manager.frontend.ports.container | int | `8000` | The port on the container for normal communications |
| love-manager.manager.frontend.ports.node | int | `30000` | The port on the node for normal communcations |
| love-manager.manager.frontend.readinessProbe | object | `{}` | Configuration for the LOVE manager frontend pods readiness probe |
| love-manager.manager.frontend.replicas | int | `1` | Set the default number of LOVE manager frontend pod replicas |
| love-manager.manager.frontend.resources | object | `{}` | Resource specifications for the LOVE manager frontend pods |
| love-manager.manager.frontend.tolerations | list | `[]` | Toleration specifications for the LOVE manager frontend pods |
| love-manager.manager.producers[0] | object | `{"affinity":{},"autoscaling":{"enabled":true,"maxReplicas":100,"minReplicas":1,"scaleDownPolicy":{},"scaleUpPolicy":{},"targetCPUUtilizationPercentage":80,"targetMemoryUtilizationPercentage":""},"env":{"AUTH_LDAP_1_SERVER_URI":"ldap://ipa1.lsst.local","AUTH_LDAP_2_SERVER_URI":"ldap://ipa2.lsst.local","AUTH_LDAP_3_SERVER_URI":"ldap://ipa3.lsst.local","COMMANDER_HOSTNAME":"love-commander-service","COMMANDER_PORT":5000,"DB_ENGINE":"postgresql","DB_HOST":"love-manager-database-service","DB_NAME":"love","DB_PORT":5432,"DB_USER":"love","HEARTBEAT_QUERY_COMMANDER":false,"JIRA_API_HOSTNAME":"rubinobs.atlassian.net","JIRA_PROJECT_ID":10063,"LOVE_SITE":"local","OLE_API_HOSTNAME":"site.lsst.local","REDIS_CONFIG_CAPACITY":5000,"REDIS_CONFIG_EXPIRY":5,"REDIS_HOST":"love-manager-redis-service","REMOTE_STORAGE":true,"SERVER_URL":"love.lsst.local","URL_SUBPATH":"/love"},"envSecrets":{"ADMIN_USER_PASS":"admin-user-pass","AUTHLIST_USER_PASS":"authlist-user-pass","AUTH_LDAP_BIND_PASSWORD":"auth-ldap-bind-password","CMD_USER_PASS":"cmd-user-pass","DB_PASS":"db-pass","JIRA_API_TOKEN":"jira-api-token","PROCESS_CONNECTION_PASS":"process-connection-pass","REDIS_PASS":"redis-pass","SECRET_KEY":"manager-secret-key","USER_USER_PASS":"user-user-pass"},"image":{"nexus3":"","pullPolicy":"IfNotPresent","repository":"lsstts/love-manager","revision":null},"name":"example-producer","nodeSelector":{},"ports":{"container":8000,"node":30000},"readinessProbe":{},"replicas":1,"resources":{},"tolerations":[]}` | Example producer configuration. Each producer should follow the same structure as frontend with the added name field. |
| love-manager.manager.producers[0].affinity | object | `{}` | Affinity rules for the LOVE manager producers pods |
| love-manager.manager.producers[0].autoscaling.enabled | bool | `true` | Whether automatic horizontal scaling is active |
| love-manager.manager.producers[0].autoscaling.maxReplicas | int | `100` | The allowed maximum number of replicas |
| love-manager.manager.producers[0].autoscaling.minReplicas | int | `1` | The allowed minimum number of replicas |
| love-manager.manager.producers[0].autoscaling.scaleDownPolicy | object | `{}` | Policy for scaling down manager pods |
| love-manager.manager.producers[0].autoscaling.scaleUpPolicy | object | `{}` | Policy for scaling up manager pods |
| love-manager.manager.producers[0].autoscaling.targetCPUUtilizationPercentage | int | `80` | The percentage of CPU utilization that will trigger the scaling |
| love-manager.manager.producers[0].autoscaling.targetMemoryUtilizationPercentage | int | `""` | The percentage of memory utilization that will trigger the scaling |
| love-manager.manager.producers[0].env.AUTH_LDAP_1_SERVER_URI | string | `"ldap://ipa1.lsst.local"` | Set the URI for the 1st LDAP server |
| love-manager.manager.producers[0].env.AUTH_LDAP_2_SERVER_URI | string | `"ldap://ipa2.lsst.local"` | Set the URI for the 2nd LDAP server |
| love-manager.manager.producers[0].env.AUTH_LDAP_3_SERVER_URI | string | `"ldap://ipa3.lsst.local"` | Set the URI for the 3rd LDAP server |
| love-manager.manager.producers[0].env.COMMANDER_HOSTNAME | string | `"love-commander-service"` | Label for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| love-manager.manager.producers[0].env.COMMANDER_PORT | int | `5000` | Port number for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| love-manager.manager.producers[0].env.DB_ENGINE | string | `"postgresql"` | The type of database engine being used for the LOVE manager producers |
| love-manager.manager.producers[0].env.DB_HOST | string | `"love-manager-database-service"` | The name of the database service |
| love-manager.manager.producers[0].env.DB_NAME | string | `"love"` | The name of the database being used for the LOVE manager producers |
| love-manager.manager.producers[0].env.DB_PORT | int | `5432` | The port for the database service |
| love-manager.manager.producers[0].env.DB_USER | string | `"love"` | The database user needed for access from the LOVE manager producers |
| love-manager.manager.producers[0].env.HEARTBEAT_QUERY_COMMANDER | bool | `false` | Have the LOVE producer managers not query commander |
| love-manager.manager.producers[0].env.JIRA_API_HOSTNAME | string | `"rubinobs.atlassian.net"` | Set the hostname for the Jira instance |
| love-manager.manager.producers[0].env.JIRA_PROJECT_ID | int | `10063` | Set the Jira project ID |
| love-manager.manager.producers[0].env.LOVE_SITE | string | `"local"` | The site tag where LOVE is being run |
| love-manager.manager.producers[0].env.OLE_API_HOSTNAME | string | `"site.lsst.local"` | Set the URL for the OLE instance |
| love-manager.manager.producers[0].env.REDIS_CONFIG_CAPACITY | int | `5000` | The connection capacity for the redis service |
| love-manager.manager.producers[0].env.REDIS_CONFIG_EXPIRY | int | `5` | The expiration time for the redis service |
| love-manager.manager.producers[0].env.REDIS_HOST | string | `"love-manager-redis-service"` | The name of the redis service |
| love-manager.manager.producers[0].env.REMOTE_STORAGE | bool | `true` | Set the manager to use LFA storage |
| love-manager.manager.producers[0].env.SERVER_URL | string | `"love.lsst.local"` | The external URL from the NGINX server for LOVE |
| love-manager.manager.producers[0].env.URL_SUBPATH | string | `"/love"` | The Kubernetes sub-path for LOVE |
| love-manager.manager.producers[0].envSecrets.ADMIN_USER_PASS | string | `"admin-user-pass"` | The LOVE manager producers admin user password secret key name |
| love-manager.manager.producers[0].envSecrets.AUTHLIST_USER_PASS | string | `"authlist-user-pass"` | The LOVE manager producers authlist_user password secret key name |
| love-manager.manager.producers[0].envSecrets.AUTH_LDAP_BIND_PASSWORD | string | `"auth-ldap-bind-password"` | The LOVE manager producers LDAP binding password secret key name |
| love-manager.manager.producers[0].envSecrets.CMD_USER_PASS | string | `"cmd-user-pass"` | The LOVE manager producers cmd_user user password secret key name |
| love-manager.manager.producers[0].envSecrets.DB_PASS | string | `"db-pass"` | The database password secret key name. Must match `database.envSecrets.POSTGRES_PASSWORD` |
| love-manager.manager.producers[0].envSecrets.JIRA_API_TOKEN | string | `"jira-api-token"` | The LOVE manager jira API token secret key name |
| love-manager.manager.producers[0].envSecrets.PROCESS_CONNECTION_PASS | string | `"process-connection-pass"` | The LOVE manager producers process connection password secret key name |
| love-manager.manager.producers[0].envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name. Must match `redis.envSecrets.REDIS_PASS` |
| love-manager.manager.producers[0].envSecrets.SECRET_KEY | string | `"manager-secret-key"` | The LOVE manager producers secret secret key name |
| love-manager.manager.producers[0].envSecrets.USER_USER_PASS | string | `"user-user-pass"` | The LOVE manager producers user user password secret key name |
| love-manager.manager.producers[0].image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| love-manager.manager.producers[0].image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE manager producers image |
| love-manager.manager.producers[0].image.repository | string | `"lsstts/love-manager"` | The LOVE manager producers image to use |
| love-manager.manager.producers[0].image.revision | int | `nil` | The cycle revision to add to the image tag |
| love-manager.manager.producers[0].nodeSelector | object | `{}` | Node selection rules for the LOVE manager producers pods |
| love-manager.manager.producers[0].ports.container | int | `8000` | The port on the container for normal communications |
| love-manager.manager.producers[0].ports.node | int | `30000` | The port on the node for normal communcations |
| love-manager.manager.producers[0].readinessProbe | object | `{}` | Configuration for the LOVE manager producers pods readiness probe |
| love-manager.manager.producers[0].replicas | int | `1` | Set the default number of LOVE manager producers pod replicas |
| love-manager.manager.producers[0].resources | object | `{}` | Resource specifications for the LOVE manager producers pods |
| love-manager.manager.producers[0].tolerations | list | `[]` | Toleration specifications for the LOVE manager producers pods |
| love-manager.manager.producers_ports | object | `{"container":8000,"node":30000}` | Configuration for the producers ports. this is a single configuration for all the producers. |
| love-manager.manager.producers_ports.container | int | `8000` | The port on the container for normal communications |
| love-manager.manager.producers_ports.node | int | `30000` | The port on the node for normal communcations |
| love-manager.namespace | string | `"love"` | The overall namespace for the application |
| love-manager.redis.affinity | object | `{}` | Affinity rules for the LOVE redis pods |
| love-manager.redis.config | string | `"timeout 60\n"` | Configuration specification for the redis service |
| love-manager.redis.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name |
| love-manager.redis.image.pullPolicy | string | `"IfNotPresent"` | The pull policy for the redis image |
| love-manager.redis.image.repository | string | `"redis"` | The redis image to use |
| love-manager.redis.image.tag | string | `"7.4.2"` | The tag to use for the redis image |
| love-manager.redis.nodeSelector | object | `{}` | Node selection rules for the LOVE redis pods |
| love-manager.redis.port | int | `6379` | The redis port number |
| love-manager.redis.resources | object | `{}` | Resource specifications for the LOVE redis pods |
| love-manager.redis.tolerations | list | `[]` | Toleration specifications for the LOVE redis pods |
| love-manager.viewBackup.affinity | object | `{}` | Affinity rules for the LOVE view backup pods |
| love-manager.viewBackup.enabled | bool | `false` | Whether view backup is active |
| love-manager.viewBackup.env | object | `{}` | Place to specify additional environment variables for the view backup job |
| love-manager.viewBackup.image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| love-manager.viewBackup.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the view backup image |
| love-manager.viewBackup.image.repository | string | `"lsstts/love-view-backup"` | The view backup image to use |
| love-manager.viewBackup.nodeSelector | object | `{}` | Node selection rules for the LOVE view backup pods |
| love-manager.viewBackup.resources | object | `{}` | Resource specifications for the LOVE view backup pods |
| love-manager.viewBackup.restartPolicy | string | `"Never"` | The restart policy type for the view backup cronjob |
| love-manager.viewBackup.schedule | string | `"0 0 1 1 *"` | The view backup job schedule in cron format |
| love-manager.viewBackup.tolerations | list | `[]` | Toleration specifications for the LOVE view backup pods |
| love-manager.viewBackup.ttlSecondsAfterFinished | string | `""` | Time after view backup job finishes before deletion (ALPHA) |
| love-nginx.affinity | object | `{}` | Affinity rules for the NGINX pod |
| love-nginx.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the NGINX image |
| love-nginx.image.repository | string | `"nginx"` | The NGINX image to use |
| love-nginx.image.tag | string | `"1.27.4"` | The tag to use for the NGINX image |
| love-nginx.imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. If this section is used, each object listed can have the following attributes defined: _name_ (The label identifying the pull-secret to use) |
| love-nginx.ingress.annotations | object | `{}` | Annotations for the NGINX ingress |
| love-nginx.ingress.className | string | `"nginx"` | Assign the Ingress class name |
| love-nginx.ingress.hostname | string | `"love.local"` | Hostname for the NGINX ingress |
| love-nginx.ingress.httpPath | string | `"/"` | Path name associated with the NGINX ingress |
| love-nginx.ingress.pathType | string | `""` | Set the Kubernetes path type for the NGINX ingress |
| love-nginx.initContainers.frontend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the frontend image |
| love-nginx.initContainers.frontend.image.repository | string | `"lsstts/love-frontend"` | The frontend image to use |
| love-nginx.initContainers.frontend.image.revision | int | `nil` | The cycle revision to add to the image tag |
| love-nginx.initContainers.manager.command | list | `["/bin/sh","-c","mkdir -p /usr/src/love-manager/media/thumbnails; mkdir -p /usr/src/love-manager/media/configs; cp -Rv /usr/src/love/manager/static /usr/src/love-manager; cp -uv /usr/src/love/manager/ui_framework/fixtures/thumbnails/* /usr/src/love-manager/media/thumbnails; cp -uv /usr/src/love/manager/api/fixtures/configs/* /usr/src/love-manager/media/configs"]` | The command to execute for the love-manager static content |
| love-nginx.initContainers.manager.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the love-manager static content image |
| love-nginx.initContainers.manager.image.repository | string | `"lsstts/love-manager"` | The static love-manager content image to use |
| love-nginx.initContainers.manager.image.revision | int | `nil` | The cycle revision to add to the image tag |
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
| love-producer.env | object | `{}` | This section holds a set of key, value pairs for environmental variables |
| love-producer.envSecrets | object | `{"PROCESS_CONNECTION_PASS":"process-connection-pass"}` | This section holds a set of key, value pairs for secrets |
| love-producer.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE producer image |
| love-producer.image.repository | string | `"lsstts/love-producer"` | The LOVE producer image to use |
| love-producer.image.revision | int | `nil` | The cycle revision to add to the image tag |
| love-producer.nodeSelector | object | `{}` | Node selection rules applied to all LOVE producer pods |
| love-producer.producers | obj | `[]` | This sections sets the list of producers to use. The producers should be specified like: _name_: The identifying name for the CSC producer _csc_: _CSC name:index_ The following attributes are optional _resources_ (A resource object specification) _nodeSelector_ (A node selector object specification) _tolerations_ (A list of tolerations) _affinity_ (An affinity object specification) |
| love-producer.replicaCount | int | `1` | Set the replica count for the LOVE producers |
| love-producer.resources | object | `{}` | Resource specifications applied to all LOVE producer pods |
| love-producer.tolerations | list | `[]` | Toleration specifications applied to all LOVE producer pods |
