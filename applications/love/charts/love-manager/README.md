# love-manager

Helm chart for the LOVE manager service.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the LOVE manager pods |
| autoscaling.enabled | bool | `true` | Whether automatic horizontal scaling is active |
| autoscaling.maxReplicas | int | `100` | The allowed maximum number of replicas |
| autoscaling.minReplicas | int | `1` | The allowed minimum number of replicas |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | The percentage of CPU utilization that will trigger the scaling |
| autoscaling.targetMemoryUtilizationPercentage | int | `""` | The percentage of memory utilization that will trigger the scaling |
| database.affinity | object | `{}` | Affinity rules for the LOVE database pods |
| database.env.POSTGRES_DB | string | `"postgres"` | Define the database type |
| database.env.POSTGRES_USER | string | `"postgres"` | Define the database user |
| database.envSecrets.POSTGRES_PASSWORD | string | `"db-pass"` | The database password secret key name |
| database.image.pullPolicy | string | `"IfNotPresent"` | The pull policy for the database image |
| database.image.repository | string | `"postgres"` | The database image to use |
| database.image.tag | string | `"12.0"` | The tag to use for the database image |
| database.nodeSelector | object | `{}` | Node selection rules for the LOVE database pods |
| database.port | int | `5432` | The database port number |
| database.resources | object | `{}` | Resource specifications for the LOVE database pods |
| database.storage.accessMode | string | `"ReadWriteMany"` | The access mode for the database storage |
| database.storage.claimSize | string | `"2Gi"` | The size of the database storage request |
| database.storage.name | string | `"love-manager-database"` | Label for the database storage point |
| database.storage.path | string | `"/var/lib/postgresql/data"` | Path within the running container |
| database.storage.storageClass | string | `"local-store"` | The storage class to request the disk allocation from |
| database.tolerations | list | `[]` | Toleration specifications for the LOVE database pods |
| env.AUTH_LDAP_1_SERVER_URI | string | `"ldap://ipa1.lsst.local"` | Set the URI for the 1st LDAP server |
| env.AUTH_LDAP_2_SERVER_URI | string | `"ldap://ipa2.lsst.local"` | Set the URI for the 2nd LDAP server |
| env.AUTH_LDAP_3_SERVER_URI | string | `"ldap://ipa3.lsst.local"` | Set the URI for the 3rd LDAP server |
| env.COMMANDER_HOSTNAME | string | `"love-commander-service"` | Label for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| env.COMMANDER_PORT | int | `5000` | Port number for the LOVE commander service. Must match the one spcified in the LOVE commander chart |
| env.DB_ENGINE | string | `"postgresql"` | The type of database engine being used for the LOVE manager |
| env.DB_HOST | string | `"love-manager-database-service"` | The name of the database service |
| env.DB_NAME | string | `"postgres"` | The name of the database being used for the LOVE manager. Must match `database.env.POSTGRES_DB` |
| env.DB_PORT | int | `5432` | The port for the database Must match `database.port` |
| env.DB_USER | string | `"postgres"` | The database user needed for access from the LOVE manager. Must match `database.env.POSTGRES_USER` |
| env.JIRA_API_HOSTNAME | string | `"jira.lsstcorp.org"` | Set the hostname for the Jira instance |
| env.JIRA_PROJECT_ID | int | `14601` | Set the Jira project ID |
| env.LOVE_PRODUCER_WEBSOCKET_HOST | string | `"love-service/manager/ws/subscription"` | The URL path for the LOVE producer websocket host |
| env.LOVE_SITE | string | `"local"` | The site tag where LOVE is being run |
| env.OLE_API_HOSTNAME | string | `"site.lsst.local"` | Set the URL for the OLE instance |
| env.REDIS_HOST | string | `"love-manager-redis-service"` | The name of the redis service |
| env.REMOTE_STORAGE | bool | `true` | Set the manager to use LFA storage |
| env.SERVER_URL | string | `"love.lsst.local"` | The external URL from the NGINX server for LOVE |
| env.URL_SUBPATH | string | `"/love"` | The Kubernetes sub-path for LOVE |
| envSecretKeyName | string | `"love"` | The top-level secret key name that houses the rest of the secrets |
| envSecrets.ADMIN_USER_PASS | string | `"admin-user-pass"` | The LOVE manager admin user password secret key name |
| envSecrets.CMD_USER_PASS | string | `"cmd-user-pass"` | The LOVE manager cmd_user user password secret key name |
| envSecrets.DB_PASS | string | `"db-pass"` | The database password secret key name. Must match `database.envSecrets.POSTGRES_PASSWORD` |
| envSecrets.PROCESS_CONNECTION_PASS | string | `"process-connection-pass"` | The LOVE manager process connection password secret key name |
| envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name. Must match `redis.envSecrets.REDIS_PASS` |
| envSecrets.SECRET_KEY | string | `"manager-secret-key"` | The LOVE manager secret secret key name |
| envSecrets.USER_USER_PASS | string | `"user-user-pass"` | The LOVE manager user user password secret key name |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the LOVE manager image |
| image.repository | string | `"lsstts/love-manager"` | The LOVE manager image to use |
| image.tag | string | `nil` |  |
| nodeSelector | object | `{}` | Node selection rules for the LOVE manager pods |
| ports.container | int | `8000` | The port on the container for normal communications |
| ports.node | int | `30000` | The port on the node for normal communcations |
| readinessProbe | object | `{}` | Configuration for the LOVE manager pods readiness probe |
| redis.affinity | object | `{}` | Affinity rules for the LOVE redis pods |
| redis.config | string | `"timeout 60\n"` | Configuration specification for the redis service |
| redis.envSecrets.REDIS_PASS | string | `"redis-pass"` | The redis password secret key name |
| redis.image.pullPolicy | string | `"IfNotPresent"` | The pull policy for the redis image |
| redis.image.repository | string | `"redis"` | The redis image to use |
| redis.image.tag | string | `"5.0.3"` | The tag to use for the redis image |
| redis.nodeSelector | object | `{}` | Node selection rules for the LOVE redis pods |
| redis.port | int | `6379` | The redis port number |
| redis.resources | object | `{}` | Resource specifications for the LOVE redis pods |
| redis.tolerations | list | `[]` | Toleration specifications for the LOVE redis pods |
| replicas | int | `1` | Set the default number of LOVE manager pod replicas |
| resources | object | `{}` | Resource specifications for the LOVE manager pods |
| tolerations | list | `[]` | Toleration specifications for the LOVE manager pods |
| viewBackup.affinity | object | `{}` | Affinity rules for the LOVE view backup pods |
| viewBackup.enabled | bool | `false` | Whether view backup is active |
| viewBackup.env | object | `{}` | Place to specify additional environment variables for the view backup job |
| viewBackup.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the view backup image |
| viewBackup.image.repository | string | `"lsstts/love-view-backup"` | The view backup image to use |
| viewBackup.image.tag | string | `"develop"` | The tag to use for the view backup image |
| viewBackup.nodeSelector | object | `{}` | Node selection rules for the LOVE view backup pods |
| viewBackup.resources | object | `{}` | Resource specifications for the LOVE view backup pods |
| viewBackup.restartPolicy | string | `"Never"` | The restart policy type for the view backup cronjob |
| viewBackup.schedule | string | `"0 0 1 1 *"` | The view backup job schedule in cron format |
| viewBackup.tolerations | list | `[]` | Toleration specifications for the LOVE view backup pods |
| viewBackup.ttlSecondsAfterFinished | string | `""` | Time after view backup job finishes before deletion (ALPHA) |
