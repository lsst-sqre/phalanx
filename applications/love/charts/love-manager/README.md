# love-manager

Helm chart for the LOVE manager service.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| manager.frontend.affinity | object | `{}` | Affinity rules for the LOVE manager frontend pods |
| manager.frontend.autoscaling.enabled | bool | `true` | Whether automatic horizontal scaling is active |
| manager.frontend.autoscaling.maxReplicas | int | `100` | The allowed maximum number of replicas |
| manager.frontend.autoscaling.minReplicas | int | `1` | The allowed minimum number of replicas |
| manager.frontend.autoscaling.scaleDownPolicy | object | `{}` | Policy for scaling down manager pods |
| manager.frontend.autoscaling.scaleUpPolicy | object | `{}` | Policy for scaling up manager pods |
| manager.frontend.autoscaling.targetCPUUtilizationPercentage | int | `80` | The percentage of CPU utilization that will trigger the scaling |
| manager.frontend.autoscaling.targetMemoryUtilizationPercentage | int | `""` | The percentage of memory utilization that will trigger the scaling |
| manager.frontend.env.AUTH_LDAP_1_SERVER_URI | string | `"ldap://ipa1.lsst.local"` | Set the URI for the 1st LDAP server |
| manager.frontend.env.AUTH_LDAP_2_SERVER_URI | string | `"ldap://ipa2.lsst.local"` | Set the URI for the 2nd LDAP server |
| manager.frontend.env.AUTH_LDAP_3_SERVER_URI | string | `"ldap://ipa3.lsst.local"` | Set the URI for the 3rd LDAP server |
| manager.frontend.env.COMMANDER_HOSTNAME | string | `"love-commander-service"` | Label for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| manager.frontend.env.COMMANDER_PORT | int | `5000` | Port number for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| manager.frontend.env.DB_ENGINE | string | `"postgresql"` | The type of database engine being used for the LOVE manager frontend |
| manager.frontend.env.DB_HOST | string | `"love-manager-database-service"` | The name of the database service |
| manager.frontend.env.DB_NAME | string | `"love"` | The name of the database being used for the LOVE manager frontend |
| manager.frontend.env.DB_PORT | int | `5432` | The port for the database service |
| manager.frontend.env.DB_USER | string | `"love"` | The database user needed for access from the LOVE manager frontend |
| manager.frontend.env.JIRA_API_HOSTNAME | string | `"jira.lsstcorp.org"` | Set the hostname for the Jira instance |
| manager.frontend.env.JIRA_PROJECT_ID | int | `14601` | Set the Jira project ID |
| manager.frontend.env.LOVE_PRODUCER_WEBSOCKET_HOST | string | `"love-service/manager/ws/subscription"` | The URL path for the LOVE producer websocket host |
| manager.frontend.env.LOVE_SITE | string | `"local"` | The site tag where LOVE is being run |
| manager.frontend.env.OLE_API_HOSTNAME | string | `"site.lsst.local"` | Set the URL for the OLE instance |
| manager.frontend.env.REDIS_CONFIG_CAPACITY | int | `5000` | The connection capacity for the redis service |
| manager.frontend.env.REDIS_CONFIG_EXPIRY | int | `5` | The expiration time for the redis service |
| manager.frontend.env.REDIS_HOST | string | `"love-manager-redis-service"` | The name of the redis service |
| manager.frontend.env.REMOTE_STORAGE | bool | `true` | Set the manager to use LFA storage |
| manager.frontend.env.SERVER_URL | string | `"love.lsst.local"` | The external URL from the NGINX server for LOVE |
| manager.frontend.env.URL_SUBPATH | string | `"/love"` | The Kubernetes sub-path for LOVE |
| manager.frontend.envSecrets.ADMIN_USER_PASS | string | `"admin-user-pass"` | The LOVE manager frontend admin user password secret key name |
| manager.frontend.envSecrets.AUTHLIST_USER_PASS | string | `"authlist-user-pass"` | The LOVE manager frontend authlist_user password secret key name |
| manager.frontend.envSecrets.AUTH_LDAP_BIND_PASSWORD | string | `"auth-ldap-bind-password"` | The LOVE manager frontend LDAP binding password secret key name |
| manager.frontend.envSecrets.CMD_USER_PASS | string | `"cmd-user-pass"` | The LOVE manager frontend cmd_user user password secret key name |
| manager.frontend.envSecrets.DB_PASS | string | `"db-pass"` | The database password secret key name. Must match `database.envSecrets.POSTGRES_PASSWORD` |
| manager.frontend.envSecrets.PROCESS_CONNECTION_PASS | string | `"process-connection-pass"` | The LOVE manager frontend process connection password secret key name |
| manager.frontend.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name. Must match `redis.envSecrets.REDIS_PASS` |
| manager.frontend.envSecrets.SECRET_KEY | string | `"manager-secret-key"` | The LOVE manager frontend secret secret key name |
| manager.frontend.envSecrets.USER_USER_PASS | string | `"user-user-pass"` | The LOVE manager frontend user user password secret key name |
| manager.frontend.image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| manager.frontend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE manager frontend image |
| manager.frontend.image.repository | string | `"lsstts/love-manager"` | The LOVE manager frontend image to use |
| manager.frontend.nodeSelector | object | `{}` | Node selection rules for the LOVE manager frontend pods |
| manager.frontend.ports.container | int | `8000` | The port on the container for normal communications |
| manager.frontend.ports.node | int | `30000` | The port on the node for normal communcations |
| manager.frontend.readinessProbe | object | `{}` | Configuration for the LOVE manager frontend pods readiness probe |
| manager.frontend.replicas | int | `1` | Set the default number of LOVE manager frontend pod replicas |
| manager.frontend.resources | object | `{}` | Resource specifications for the LOVE manager frontend pods |
| manager.frontend.tolerations | list | `[]` | Toleration specifications for the LOVE manager frontend pods |
| manager.producers.affinity | object | `{}` | Affinity rules for the LOVE manager producers pods |
| manager.producers.autoscaling.enabled | bool | `true` | Whether automatic horizontal scaling is active |
| manager.producers.autoscaling.maxReplicas | int | `100` | The allowed maximum number of replicas |
| manager.producers.autoscaling.minReplicas | int | `1` | The allowed minimum number of replicas |
| manager.producers.autoscaling.scaleDownPolicy | object | `{}` | Policy for scaling down manager pods |
| manager.producers.autoscaling.scaleUpPolicy | object | `{}` | Policy for scaling up manager pods |
| manager.producers.autoscaling.targetCPUUtilizationPercentage | int | `80` | The percentage of CPU utilization that will trigger the scaling |
| manager.producers.autoscaling.targetMemoryUtilizationPercentage | int | `""` | The percentage of memory utilization that will trigger the scaling |
| manager.producers.env.AUTH_LDAP_1_SERVER_URI | string | `"ldap://ipa1.lsst.local"` | Set the URI for the 1st LDAP server |
| manager.producers.env.AUTH_LDAP_2_SERVER_URI | string | `"ldap://ipa2.lsst.local"` | Set the URI for the 2nd LDAP server |
| manager.producers.env.AUTH_LDAP_3_SERVER_URI | string | `"ldap://ipa3.lsst.local"` | Set the URI for the 3rd LDAP server |
| manager.producers.env.COMMANDER_HOSTNAME | string | `"love-commander-service"` | Label for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| manager.producers.env.COMMANDER_PORT | int | `5000` | Port number for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| manager.producers.env.DB_ENGINE | string | `"postgresql"` | The type of database engine being used for the LOVE manager producers |
| manager.producers.env.DB_HOST | string | `"love-manager-database-service"` | The name of the database service |
| manager.producers.env.DB_NAME | string | `"love"` | The name of the database being used for the LOVE manager producers |
| manager.producers.env.DB_PORT | int | `5432` | The port for the database service |
| manager.producers.env.DB_USER | string | `"love"` | The database user needed for access from the LOVE manager producers |
| manager.producers.env.HEARTBEAT_QUERY_COMMANDER | bool | `false` | Have the LOVE producer managers not query commander |
| manager.producers.env.JIRA_API_HOSTNAME | string | `"jira.lsstcorp.org"` | Set the hostname for the Jira instance |
| manager.producers.env.JIRA_PROJECT_ID | int | `14601` | Set the Jira project ID |
| manager.producers.env.LOVE_SITE | string | `"local"` | The site tag where LOVE is being run |
| manager.producers.env.OLE_API_HOSTNAME | string | `"site.lsst.local"` | Set the URL for the OLE instance |
| manager.producers.env.REDIS_CONFIG_CAPACITY | int | `5000` | The connection capacity for the redis service |
| manager.producers.env.REDIS_CONFIG_EXPIRY | int | `5` | The expiration time for the redis service |
| manager.producers.env.REDIS_HOST | string | `"love-manager-redis-service"` | The name of the redis service |
| manager.producers.env.REMOTE_STORAGE | bool | `true` | Set the manager to use LFA storage |
| manager.producers.env.SERVER_URL | string | `"love.lsst.local"` | The external URL from the NGINX server for LOVE |
| manager.producers.env.URL_SUBPATH | string | `"/love"` | The Kubernetes sub-path for LOVE |
| manager.producers.envSecrets.ADMIN_USER_PASS | string | `"admin-user-pass"` | The LOVE manager producers admin user password secret key name |
| manager.producers.envSecrets.AUTHLIST_USER_PASS | string | `"authlist-user-pass"` | The LOVE manager producers authlist_user password secret key name |
| manager.producers.envSecrets.AUTH_LDAP_BIND_PASSWORD | string | `"auth-ldap-bind-password"` | The LOVE manager producers LDAP binding password secret key name |
| manager.producers.envSecrets.CMD_USER_PASS | string | `"cmd-user-pass"` | The LOVE manager producers cmd_user user password secret key name |
| manager.producers.envSecrets.DB_PASS | string | `"db-pass"` | The database password secret key name. Must match `database.envSecrets.POSTGRES_PASSWORD` |
| manager.producers.envSecrets.PROCESS_CONNECTION_PASS | string | `"process-connection-pass"` | The LOVE manager producers process connection password secret key name |
| manager.producers.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name. Must match `redis.envSecrets.REDIS_PASS` |
| manager.producers.envSecrets.SECRET_KEY | string | `"manager-secret-key"` | The LOVE manager producers secret secret key name |
| manager.producers.envSecrets.USER_USER_PASS | string | `"user-user-pass"` | The LOVE manager producers user user password secret key name |
| manager.producers.image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| manager.producers.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE manager producers image |
| manager.producers.image.repository | string | `"lsstts/love-manager"` | The LOVE manager producers image to use |
| manager.producers.nodeSelector | object | `{}` | Node selection rules for the LOVE manager producers pods |
| manager.producers.ports.container | int | `8000` | The port on the container for normal communications |
| manager.producers.ports.node | int | `30000` | The port on the node for normal communcations |
| manager.producers.readinessProbe | object | `{}` | Configuration for the LOVE manager producers pods readiness probe |
| manager.producers.replicas | int | `1` | Set the default number of LOVE manager producers pod replicas |
| manager.producers.resources | object | `{}` | Resource specifications for the LOVE manager producers pods |
| manager.producers.tolerations | list | `[]` | Toleration specifications for the LOVE manager producers pods |
| namespace | string | `"love"` | The overall namespace for the application |
| redis.affinity | object | `{}` | Affinity rules for the LOVE redis pods |
| redis.config | string | `"timeout 60\n"` | Configuration specification for the redis service |
| redis.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name |
| redis.image.pullPolicy | string | `"IfNotPresent"` | The pull policy for the redis image |
| redis.image.repository | string | `"redis"` | The redis image to use |
| redis.image.tag | string | `"7.2.4"` | The tag to use for the redis image |
| redis.nodeSelector | object | `{}` | Node selection rules for the LOVE redis pods |
| redis.port | int | `6379` | The redis port number |
| redis.resources | object | `{}` | Resource specifications for the LOVE redis pods |
| redis.tolerations | list | `[]` | Toleration specifications for the LOVE redis pods |
| viewBackup.affinity | object | `{}` | Affinity rules for the LOVE view backup pods |
| viewBackup.enabled | bool | `false` | Whether view backup is active |
| viewBackup.env | object | `{}` | Place to specify additional environment variables for the view backup job |
| viewBackup.image.nexus3 | string | `""` | The tag name for the Nexus3 Docker repository secrets if private images need to be pulled |
| viewBackup.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the view backup image |
| viewBackup.image.repository | string | `"lsstts/love-view-backup"` | The view backup image to use |
| viewBackup.nodeSelector | object | `{}` | Node selection rules for the LOVE view backup pods |
| viewBackup.resources | object | `{}` | Resource specifications for the LOVE view backup pods |
| viewBackup.restartPolicy | string | `"Never"` | The restart policy type for the view backup cronjob |
| viewBackup.schedule | string | `"0 0 1 1 *"` | The view backup job schedule in cron format |
| viewBackup.tolerations | list | `[]` | Toleration specifications for the LOVE view backup pods |
| viewBackup.ttlSecondsAfterFinished | string | `""` | Time after view backup job finishes before deletion (ALPHA) |
