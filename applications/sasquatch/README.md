# sasquatch

Rubin Observatory's telemetry service

**Homepage:** <https://sasquatch.lsst.io/>

## Source Code

* <https://github.com/influxdata/influxdb>
* <https://github.com/obsidiandynamics/kafdrop>
* <https://github.com/confluentinc/kafka-rest>
* <https://github.com/lsst-sqre/sasquatch>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| app-metrics.apps | list | `[]` | The apps to create configuration for. |
| app-metrics.enabled | bool | `false` | Enable the app-metrics subchart with topic, user, and telegraf configurations |
| backpack.enabled | bool | `false` | Whether to enable the backpack subchart |
| backup.enabled | bool | `false` | Whether to enable the backups subchart |
| chronograf.enabled | bool | `true` | Whether to enable Chronograf |
| chronograf.env | object | See `values.yaml` | Additional environment variables for Chronograf |
| chronograf.envFromSecret | string | `"sasquatch"` | Name of secret to use. The keys `generic_client_id`, `generic_client_secret`, and `token_secret` should be set. |
| chronograf.image.repository | string | `"quay.io/influxdb/chronograf"` | Docker image to use for Chronograf |
| chronograf.image.tag | string | `"1.10.6"` | Docker tag to use for Chronograf |
| chronograf.ingress.className | string | `"nginx"` | Ingress class to use |
| chronograf.ingress.enabled | bool | `false` | Whether to enable the Chronograf ingress |
| chronograf.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the ingress |
| chronograf.ingress.path | string | `"/chronograf"` | Path for the ingress |
| chronograf.ingress.tls | bool | `false` | Whether to obtain TLS certificates for the ingress hostname |
| chronograf.persistence.enabled | bool | `true` | Whether to enable persistence for Chronograf data |
| chronograf.persistence.size | string | `"100Gi"` | Size of data store to request, if enabled |
| chronograf.resources | object | See `values.yaml` | Kubernetes resource requests and limits for Chronograf |
| chronograf.updateStrategy.type | string | `"Recreate"` | Deployment strategy, use recreate with persistence enabled |
| consdb.enabled | bool | `false` | Whether to enable the consdb subchart |
| control-system.enabled | bool | `false` | Whether to enable the control-system subchart |
| customInfluxDBIngress.annotations | object | See `values.yaml` | Annotations to add to the ingress |
| customInfluxDBIngress.enabled | bool | `false` | Whether to enable the custom ingress for InfluxDB OSS |
| customInfluxDBIngress.hostname | string | None, must be set if the ingress is enabled | Hostname of the ingress |
| customInfluxDBIngress.path | string | `"/influxdb(/\|$)(.*)"` | Path for the ingress |
| influxdb-enterprise-standby.enabled | bool | `false` | Whether to enable influxdb-enterprise-standby |
| influxdb-enterprise.enabled | bool | `false` | Whether to enable influxdb-enterprise |
| influxdb.config.continuous_queries.enabled | bool | `false` | Whether continuous queries are enabled |
| influxdb.config.coordinator.log-queries-after | string | `"15s"` | Maximum duration a query can run before InfluxDB logs it as a slow query |
| influxdb.config.coordinator.max-concurrent-queries | int | `500` | Maximum number of running queries allowed on the instance (0 is unlimited) |
| influxdb.config.coordinator.query-timeout | string | `"15s"` | Maximum duration a query is allowed to run before it is killed |
| influxdb.config.coordinator.write-timeout | string | `"1h"` | Duration a write request waits before timeout is returned to the caller |
| influxdb.config.data.cache-max-memory-size | int | `0` | Maximum size a shared cache can reach before it starts rejecting writes |
| influxdb.config.data.max-series-per-database | int | `0` | Maximum number of series allowed per database before writes are dropped. Change the setting to 0 to allow an unlimited number of series per database. |
| influxdb.config.data.trace-logging-enabled | bool | `true` | Whether to enable verbose logging of additional debug information within the TSM engine and WAL |
| influxdb.config.data.wal-fsync-delay | string | `"100ms"` | Duration a write will wait before fsyncing. This is useful for slower disks or when WAL write contention is present. |
| influxdb.config.http.auth-enabled | bool | `true` | Whether authentication is required |
| influxdb.config.http.enabled | bool | `true` | Whether to enable the HTTP endpoints |
| influxdb.config.http.flux-enabled | bool | `true` | Whether to enable the Flux query endpoint |
| influxdb.config.http.max-row-limit | int | `0` | Maximum number of rows the system can return from a non-chunked query (0 is unlimited) |
| influxdb.config.logging.level | string | `"debug"` | Logging level |
| influxdb.enabled | bool | `true` | Whether InfluxDB is enabled |
| influxdb.image.tag | string | `"1.11.8"` | InfluxDB image tag |
| influxdb.ingress.annotations | object | See `values.yaml` | Annotations to add to the ingress |
| influxdb.ingress.className | string | `"nginx"` | Ingress class to use |
| influxdb.ingress.enabled | bool | `false` | Whether to enable the InfluxDB ingress |
| influxdb.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the ingress |
| influxdb.ingress.path | string | `"/influxdb(/\|$)(.*)"` | Path for the ingress |
| influxdb.ingress.tls | bool | `false` | Whether to obtain TLS certificates for the ingress hostname |
| influxdb.initScripts.enabled | bool | `false` | Whether to enable the InfluxDB custom initialization script |
| influxdb.livenessProbe.initialDelaySeconds | int | `90` | Liveness probe initial delay in seconds |
| influxdb.persistence.enabled | bool | `true` | Whether to use persistent volume claims. By default, `storageClass` is undefined, choosing the default provisioner (standard on GKE). |
| influxdb.persistence.size | string | 1TiB for teststand deployments | Persistent volume size |
| influxdb.resources | object | See `values.yaml` | Kubernetes resource requests and limits |
| influxdb.securityContext.fsGroup | int | `1500` |  |
| influxdb.securityContext.runAsGroup | int | `1500` |  |
| influxdb.securityContext.runAsNonRoot | bool | `true` |  |
| influxdb.securityContext.runAsUser | int | `1500` |  |
| influxdb.setDefaultUser.enabled | bool | `true` | Whether the default InfluxDB user is set |
| influxdb.setDefaultUser.user.existingSecret | string | `"sasquatch"` | Use `influxdb-user` and `influxdb-password` keys from this secret |
| kafdrop.enabled | bool | `true` | Whether to enable the kafdrop subchart |
| kafka-connect-manager.enabled | bool | `false` | Whether to enable the Kafka Connect Manager |
| kapacitor.enabled | bool | `true` | Whether to enable Kapacitor |
| kapacitor.envVars | object | See `values.yaml` | Additional environment variables to set |
| kapacitor.existingSecret | string | `"sasquatch"` | Use `influxdb-user` and `influxdb-password` keys from this secret |
| kapacitor.image.repository | string | `"kapacitor"` | Docker image to use for Kapacitor |
| kapacitor.image.tag | string | `"1.7.6"` | Tag to use for Kapacitor |
| kapacitor.influxURL | string | `"http://sasquatch-influxdb.sasquatch:8086"` | InfluxDB connection URL |
| kapacitor.persistence.enabled | bool | `true` | Whether to enable Kapacitor data persistence |
| kapacitor.persistence.size | string | `"100Gi"` | Size of storage to request if enabled |
| kapacitor.resources | object | See `values.yaml` | Kubernetes resource requests and limits for Kapacitor |
| kapacitor.strategy.type | string | `"Recreate"` | Deployment strategy, use recreate with persistence enabled |
| obsenv.enabled | bool | `false` | Whether to enable the obsenv subchart |
| obsloctap.enabled | bool | `false` | Whether to enable the obsloctap subchart |
| prompt-processing.enabled | bool | `false` | Whether to enable the prompt-processing subchart |
| rest-proxy.enabled | bool | `false` | Whether to enable the REST proxy |
| squareEvents.enabled | bool | `false` | Enable the Square Events subchart with topic and user configurations |
| strimzi-kafka.connect.enabled | bool | `true` | Whether Kafka Connect is enabled |
| strimzi-kafka.kafka.listeners.external.enabled | bool | `true` | Whether external listener is enabled |
| strimzi-kafka.kafka.listeners.plain.enabled | bool | `true` | Whether internal plaintext listener is enabled |
| strimzi-kafka.kafka.listeners.tls.enabled | bool | `true` | Whether internal TLS listener is enabled |
| strimzi-registry-operator.clusterName | string | `"sasquatch"` | Name of the Strimzi Kafka cluster |
| strimzi-registry-operator.clusterNamespace | string | `"sasquatch"` | Namespace where the Strimzi Kafka cluster is deployed |
| strimzi-registry-operator.operatorNamespace | string | `"sasquatch"` | Namespace where the strimzi-registry-operator is deployed |
| tap.enabled | bool | `false` | Whether to enable the tap subchart |
| telegraf.enabled | bool | `false` | Whether to enable the telegraf subchart |
| app-metrics.affinity | object | `{}` | Affinity for pod assignment |
| app-metrics.apps | list | `[]` | A list of applications that will publish metrics events, and the keys that should be ingested into InfluxDB as tags.  The names should be the same as the app names in Phalanx. |
| app-metrics.args | list | `[]` | Arguments passed to the Telegraf agent containers |
| app-metrics.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| app-metrics.debug | bool | false | Run Telegraf in debug mode. |
| app-metrics.env | list | See `values.yaml` | Telegraf agent enviroment variables |
| app-metrics.envFromSecret | string | `""` | Name of the secret with values to be added to the environment |
| app-metrics.globalAppConfig | object | See `values.yaml` | app-metrics configuration in any environment in which the subchart is enabled. This should stay globally specified here, and it shouldn't be overridden.  See [here](https://sasquatch.lsst.io/user-guide/app-metrics.html#configuration) for the structure of this value. |
| app-metrics.globalInfluxTags | list | `["application"]` | Keys in an every event sent by any app that should be recorded in InfluxDB as "tags" (vs. "fields"). These will be concatenated with the `influxTags` from `globalAppConfig` |
| app-metrics.image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| app-metrics.image.repo | string | `"docker.io/library/telegraf"` | Telegraf image repository |
| app-metrics.image.tag | string | `"1.34.0-alpine"` | Telegraf image tag |
| app-metrics.imagePullSecrets | list | `[]` | Secret names to use for Docker pulls |
| app-metrics.influxdb.url | string | `"http://sasquatch-influxdb.sasquatch:8086"` | URL of the InfluxDB v1 instance to write to |
| app-metrics.nodeSelector | object | `{}` | Node labels for pod assignment |
| app-metrics.podAnnotations | object | `{}` | Annotations for the Telegraf pods |
| app-metrics.podLabels | object | `{}` | Labels for the Telegraf pods |
| app-metrics.replicaCount | int | `3` | Number of Telegraf replicas. Multiple replicas increase availability. |
| app-metrics.resources | object | See `values.yaml` | Kubernetes resources requests and limits |
| app-metrics.tolerations | list | `[]` | Tolerations for pod assignment |
| backpack.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| backup.affinity | object | `{}` | Affinity rules for the backups deployment pod |
| backup.backupItems | list | `[{"enabled":false,"name":"chronograf","retentionDays":7},{"enabled":false,"name":"kapacitor","retentionDays":7},{"enabled":false,"name":"influxdb-enterprise-incremental"},{"enabled":false,"name":"influxdb-oss-full","retentionDays":3}]` | List of items to backup using the sasquatch backup script |
| backup.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the backups image |
| backup.image.repository | string | `"ghcr.io/lsst-sqre/sasquatch"` | Image to use in the backups deployment |
| backup.image.tag | string | The appVersion of the chart | Tag of image to use |
| backup.nodeSelector | object | `{}` | Node selection rules for the backups deployment pod |
| backup.persistence.size | string | "100Gi" | Size of the data store to request, if enabled |
| backup.persistence.storageClass | string | "" (empty string) to use the cluster default storage class | Storage class to use for the backups |
| backup.podAnnotations | object | `{}` | Annotations for the backups deployment pod |
| backup.resources | object | `{}` | Resource limits and requests for the backups deployment pod |
| backup.schedule | string | "0 3 * * *" | Schedule for executing the sasquatch backup script |
| backup.tolerations | list | `[]` | Tolerations for the backups deployment pod |
| consdb.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| control-system.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| control-system.topics | list | `[]` | Create lsst.s3.* related topics for the ts-salkafka user. |
| influxdb-enterprise.bootstrap.auth.secretName | string | `"sasquatch"` | Enable authentication of the data nodes using this secret, by creating a username and password for an admin account. The secret must contain keys `username` and `password`. |
| influxdb-enterprise.bootstrap.ddldml.configMap | string | Do not run DDL or DML | A config map containing DDL and DML that define databases, retention policies, and inject some data.  The keys `ddl` and `dml` must exist, even if one of them is empty.  DDL is executed before DML to ensure databases and retention policies exist. |
| influxdb-enterprise.bootstrap.ddldml.resources | object | `{}` | Kubernetes resources and limits for the bootstrap job |
| influxdb-enterprise.data.affinity | object | See `values.yaml` | Affinity rules for data pods |
| influxdb-enterprise.data.config.antiEntropy.enabled | bool | `false` | Enable the anti-entropy service, which copies and repairs shards |
| influxdb-enterprise.data.config.cluster.log-queries-after | string | `"15s"` | Maximum duration a query can run before InfluxDB logs it as a slow query |
| influxdb-enterprise.data.config.cluster.max-concurrent-queries | int | `1000` | Maximum number of running queries allowed on the instance (0 is unlimited) |
| influxdb-enterprise.data.config.cluster.query-timeout | string | `"300s"` | Maximum duration a query is allowed to run before it is killed |
| influxdb-enterprise.data.config.continuousQueries.enabled | bool | `false` | Whether continuous queries are enabled |
| influxdb-enterprise.data.config.data.cache-max-memory-size | int | `0` | Maximum size a shared cache can reach before it starts rejecting writes |
| influxdb-enterprise.data.config.data.trace-logging-enabled | bool | `true` | Whether to enable verbose logging of additional debug information within the TSM engine and WAL |
| influxdb-enterprise.data.config.data.wal-fsync-delay | string | `"100ms"` | Duration a write will wait before fsyncing. This is useful for slower disks or when WAL write contention is present. |
| influxdb-enterprise.data.config.hintedHandoff.max-size | int | `107374182400` | Maximum size of the hinted-handoff queue in bytes |
| influxdb-enterprise.data.config.http.auth-enabled | bool | `true` | Whether authentication is required |
| influxdb-enterprise.data.config.http.flux-enabled | bool | `true` | Whether to enable the Flux query endpoint |
| influxdb-enterprise.data.config.logging.level | string | `"debug"` | Logging level |
| influxdb-enterprise.data.env | object | `{}` | Additional environment variables to set in the meta container |
| influxdb-enterprise.data.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for data images |
| influxdb-enterprise.data.image.repository | string | `"influxdb"` | Docker repository for data images |
| influxdb-enterprise.data.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the data ingress |
| influxdb-enterprise.data.ingress.className | string | `"nginx"` | Ingress class name of the data service |
| influxdb-enterprise.data.ingress.enabled | bool | `false` | Whether to enable an ingress for the data service |
| influxdb-enterprise.data.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the data ingress |
| influxdb-enterprise.data.ingress.path | string | `"/influxdb-enterprise-data(/\|$)(.*)"` | Path of the data service |
| influxdb-enterprise.data.nodeSelector | object | `{}` | Node selection rules for data pods |
| influxdb-enterprise.data.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for the persistent volume claim |
| influxdb-enterprise.data.persistence.annotations | object | `{}` | Annotations to add to the persistent volume claim |
| influxdb-enterprise.data.persistence.enabled | bool | `false` | Whether to persist data to a persistent volume |
| influxdb-enterprise.data.persistence.existingClaim | string | Use a volume claim template | Manually managed PersistentVolumeClaim to use. If defined, this PVC must be created manually before the meta service will start |
| influxdb-enterprise.data.persistence.size | string | `"8Gi"` | Size of persistent volume to request |
| influxdb-enterprise.data.persistence.storageClass | string | `""` | Storage class of the persistent volume (set to `-` to disable dynamic provisioning, leave unset to use the default provisioner |
| influxdb-enterprise.data.podAnnotations | object | `{}` | Annotations for data pods |
| influxdb-enterprise.data.podDisruptionBudget.minAvailable | int | `1` | Minimum available pods to maintain |
| influxdb-enterprise.data.podSecurityContext | object | `{}` | Pod security context for data pods |
| influxdb-enterprise.data.preruncmds | list | `[]` | Commands to run in data pods before InfluxDB is started. Each list entry should have a _cmd_ key with the command to run and an optional _description_ key describing that command |
| influxdb-enterprise.data.replicas | int | `1` | Number of data replicas to run |
| influxdb-enterprise.data.resources | object | `{}` | Kubernetes resources and limits for the meta container |
| influxdb-enterprise.data.securityContext | object | `{}` | Security context for meta pods |
| influxdb-enterprise.data.service.annotations | object | `{}` | Extra annotations for the data service |
| influxdb-enterprise.data.service.externalIPs | list | Do not allocate external IPs | External IPs for the data service |
| influxdb-enterprise.data.service.externalTrafficPolicy | string | Do not set an external traffic policy | External traffic policy for the data service |
| influxdb-enterprise.data.service.loadBalancerIP | string | Do not allocate a load balancer IP | Load balancer IP for the data service |
| influxdb-enterprise.data.service.nodePort | int | Do not allocate a node port | Node port for the data service |
| influxdb-enterprise.data.service.type | string | `"ClusterIP"` | Service type for the data service |
| influxdb-enterprise.data.tolerations | list | `[]` | Tolerations for data pods |
| influxdb-enterprise.envFromSecret | string | No secret | The name of a secret in the same kubernetes namespace which contain values to be added to the environment |
| influxdb-enterprise.fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| influxdb-enterprise.image.addsuffix | bool | `false` | Set to true to add a suffix for the type of image to the Docker tag (for example, `-meta`, making an image name of `influxdb:1.8.0-meta`) |
| influxdb-enterprise.image.tag | string | `appVersion` from `Chart.yaml` | Tagged version of the Docker image that you want to run |
| influxdb-enterprise.imagePullSecrets | list | `[]` | List of pull secrets needed for images. If set, each object in the list should have one attribute, _name_, identifying the pull secret to use |
| influxdb-enterprise.license.key | string | `""` | License key. You can put your license key here for testing this chart out, but we STRONGLY recommend using a license file stored in a secret when you ship to production. |
| influxdb-enterprise.license.secret.key | string | `"json"` | Key within that secret that contains the license |
| influxdb-enterprise.license.secret.name | string | `"influxdb-enterprise-license"` | Name of the secret containing the license |
| influxdb-enterprise.meta.affinity | object | See `values.yaml` | Affinity rules for meta pods |
| influxdb-enterprise.meta.env | object | `{}` | Additional environment variables to set in the meta container |
| influxdb-enterprise.meta.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for meta images |
| influxdb-enterprise.meta.image.repository | string | `"influxdb"` | Docker repository for meta images |
| influxdb-enterprise.meta.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the meta ingress |
| influxdb-enterprise.meta.ingress.className | string | `"nginx"` | Ingress class name of the meta service |
| influxdb-enterprise.meta.ingress.enabled | bool | `false` | Whether to enable an ingress for the meta service |
| influxdb-enterprise.meta.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the meta ingress |
| influxdb-enterprise.meta.ingress.path | string | `"/influxdb-enterprise-meta(/\|$)(.*)"` | Path of the meta service |
| influxdb-enterprise.meta.nodeSelector | object | `{}` | Node selection rules for meta pods |
| influxdb-enterprise.meta.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for the persistent volume claim |
| influxdb-enterprise.meta.persistence.annotations | object | `{}` | Annotations to add to the persistent volume claim |
| influxdb-enterprise.meta.persistence.enabled | bool | `false` | Whether to persist data to a persistent volume |
| influxdb-enterprise.meta.persistence.existingClaim | string | Use a volume claim template | Manually managed PersistentVolumeClaim to use. If defined, this PVC must be created manually before the meta service will start |
| influxdb-enterprise.meta.persistence.size | string | `"8Gi"` | Size of persistent volume to request |
| influxdb-enterprise.meta.persistence.storageClass | string | `""` | Storage class of the persistent volume (set to `-` to disable dynamic provisioning, leave unset to use the default provisioner |
| influxdb-enterprise.meta.podAnnotations | object | `{}` | Annotations for meta pods |
| influxdb-enterprise.meta.podDisruptionBudget.minAvailable | int | `2` | Minimum available pods to maintain |
| influxdb-enterprise.meta.podSecurityContext | object | `{}` | Pod security context for meta pods |
| influxdb-enterprise.meta.preruncmds | list | `[]` | Commands to run in meta pods before InfluxDB is started. Each list entry should have a _cmd_ key with the command to run and an optional _description_ key describing that command |
| influxdb-enterprise.meta.replicas | int | `3` | Number of meta pods to run |
| influxdb-enterprise.meta.resources | object | `{}` | Kubernetes resources and limits for the meta container |
| influxdb-enterprise.meta.securityContext | object | `{}` | Security context for meta pods |
| influxdb-enterprise.meta.service.annotations | object | `{}` | Extra annotations for the meta service |
| influxdb-enterprise.meta.service.externalIPs | list | Do not allocate external IPs | External IPs for the meta service |
| influxdb-enterprise.meta.service.externalTrafficPolicy | string | Do not set an external traffic policy | External traffic policy for the meta service |
| influxdb-enterprise.meta.service.loadBalancerIP | string | Do not allocate a load balancer IP | Load balancer IP for the meta service |
| influxdb-enterprise.meta.service.nodePort | int | Do not allocate a node port | Node port for the meta service |
| influxdb-enterprise.meta.service.type | string | `"ClusterIP"` | Service type for the meta service |
| influxdb-enterprise.meta.sharedSecret.secret | object | `{"key":"secret","name":"influxdb-enterprise-shared-secret"}` | Shared secret used by the internal API for JWT authentication between InfluxDB nodes. Must have a key named `secret` that should be a long, random string See [documentation for shared-internal-secret](https://docs.influxdata.com/enterprise_influxdb/v1/administration/configure/config-data-nodes/#meta-internal-shared-secret). |
| influxdb-enterprise.meta.sharedSecret.secret.key | string | `"secret"` | Key within that secret that contains the shared secret |
| influxdb-enterprise.meta.sharedSecret.secret.name | string | `"influxdb-enterprise-shared-secret"` | Name of the secret containing the shared secret |
| influxdb-enterprise.meta.tolerations | list | `[]` | Tolerations for meta pods |
| influxdb-enterprise.nameOverride | string | `""` | Override the base name for resources |
| influxdb-enterprise.serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| influxdb-enterprise.serviceAccount.create | bool | `false` | Whether to create a Kubernetes service account to run as |
| influxdb-enterprise.serviceAccount.name | string | Name based on the chart fullname | Name of the Kubernetes service account to run as |
| influxdb-enterprise-active.bootstrap.auth.secretName | string | `"sasquatch"` | Enable authentication of the data nodes using this secret, by creating a username and password for an admin account. The secret must contain keys `username` and `password`. |
| influxdb-enterprise-active.bootstrap.ddldml.configMap | string | Do not run DDL or DML | A config map containing DDL and DML that define databases, retention policies, and inject some data.  The keys `ddl` and `dml` must exist, even if one of them is empty.  DDL is executed before DML to ensure databases and retention policies exist. |
| influxdb-enterprise-active.bootstrap.ddldml.resources | object | `{}` | Kubernetes resources and limits for the bootstrap job |
| influxdb-enterprise-active.data.affinity | object | See `values.yaml` | Affinity rules for data pods |
| influxdb-enterprise-active.data.config.antiEntropy.enabled | bool | `false` | Enable the anti-entropy service, which copies and repairs shards |
| influxdb-enterprise-active.data.config.cluster.log-queries-after | string | `"15s"` | Maximum duration a query can run before InfluxDB logs it as a slow query |
| influxdb-enterprise-active.data.config.cluster.max-concurrent-queries | int | `1000` | Maximum number of running queries allowed on the instance (0 is unlimited) |
| influxdb-enterprise-active.data.config.cluster.query-timeout | string | `"300s"` | Maximum duration a query is allowed to run before it is killed |
| influxdb-enterprise-active.data.config.continuousQueries.enabled | bool | `false` | Whether continuous queries are enabled |
| influxdb-enterprise-active.data.config.data.cache-max-memory-size | int | `0` | Maximum size a shared cache can reach before it starts rejecting writes |
| influxdb-enterprise-active.data.config.data.trace-logging-enabled | bool | `true` | Whether to enable verbose logging of additional debug information within the TSM engine and WAL |
| influxdb-enterprise-active.data.config.data.wal-fsync-delay | string | `"100ms"` | Duration a write will wait before fsyncing. This is useful for slower disks or when WAL write contention is present. |
| influxdb-enterprise-active.data.config.hintedHandoff.max-size | int | `107374182400` | Maximum size of the hinted-handoff queue in bytes |
| influxdb-enterprise-active.data.config.http.auth-enabled | bool | `true` | Whether authentication is required |
| influxdb-enterprise-active.data.config.http.flux-enabled | bool | `true` | Whether to enable the Flux query endpoint |
| influxdb-enterprise-active.data.config.logging.level | string | `"debug"` | Logging level |
| influxdb-enterprise-active.data.env | object | `{}` | Additional environment variables to set in the meta container |
| influxdb-enterprise-active.data.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for data images |
| influxdb-enterprise-active.data.image.repository | string | `"influxdb"` | Docker repository for data images |
| influxdb-enterprise-active.data.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the data ingress |
| influxdb-enterprise-active.data.ingress.className | string | `"nginx"` | Ingress class name of the data service |
| influxdb-enterprise-active.data.ingress.enabled | bool | `false` | Whether to enable an ingress for the data service |
| influxdb-enterprise-active.data.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the data ingress |
| influxdb-enterprise-active.data.ingress.path | string | `"/influxdb-enterprise-data(/\|$)(.*)"` | Path of the data service |
| influxdb-enterprise-active.data.nodeSelector | object | `{}` | Node selection rules for data pods |
| influxdb-enterprise-active.data.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for the persistent volume claim |
| influxdb-enterprise-active.data.persistence.annotations | object | `{}` | Annotations to add to the persistent volume claim |
| influxdb-enterprise-active.data.persistence.enabled | bool | `false` | Whether to persist data to a persistent volume |
| influxdb-enterprise-active.data.persistence.existingClaim | string | Use a volume claim template | Manually managed PersistentVolumeClaim to use. If defined, this PVC must be created manually before the meta service will start |
| influxdb-enterprise-active.data.persistence.size | string | `"8Gi"` | Size of persistent volume to request |
| influxdb-enterprise-active.data.persistence.storageClass | string | `""` | Storage class of the persistent volume (set to `-` to disable dynamic provisioning, leave unset to use the default provisioner |
| influxdb-enterprise-active.data.podAnnotations | object | `{}` | Annotations for data pods |
| influxdb-enterprise-active.data.podDisruptionBudget.minAvailable | int | `1` | Minimum available pods to maintain |
| influxdb-enterprise-active.data.podSecurityContext | object | `{}` | Pod security context for data pods |
| influxdb-enterprise-active.data.preruncmds | list | `[]` | Commands to run in data pods before InfluxDB is started. Each list entry should have a _cmd_ key with the command to run and an optional _description_ key describing that command |
| influxdb-enterprise-active.data.replicas | int | `1` | Number of data replicas to run |
| influxdb-enterprise-active.data.resources | object | `{}` | Kubernetes resources and limits for the meta container |
| influxdb-enterprise-active.data.securityContext | object | `{}` | Security context for meta pods |
| influxdb-enterprise-active.data.service.annotations | object | `{}` | Extra annotations for the data service |
| influxdb-enterprise-active.data.service.externalIPs | list | Do not allocate external IPs | External IPs for the data service |
| influxdb-enterprise-active.data.service.externalTrafficPolicy | string | Do not set an external traffic policy | External traffic policy for the data service |
| influxdb-enterprise-active.data.service.loadBalancerIP | string | Do not allocate a load balancer IP | Load balancer IP for the data service |
| influxdb-enterprise-active.data.service.nodePort | int | Do not allocate a node port | Node port for the data service |
| influxdb-enterprise-active.data.service.type | string | `"ClusterIP"` | Service type for the data service |
| influxdb-enterprise-active.data.tolerations | list | `[]` | Tolerations for data pods |
| influxdb-enterprise-active.envFromSecret | string | No secret | The name of a secret in the same kubernetes namespace which contain values to be added to the environment |
| influxdb-enterprise-active.fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| influxdb-enterprise-active.image.addsuffix | bool | `false` | Set to true to add a suffix for the type of image to the Docker tag (for example, `-meta`, making an image name of `influxdb:1.8.0-meta`) |
| influxdb-enterprise-active.image.tag | string | `appVersion` from `Chart.yaml` | Tagged version of the Docker image that you want to run |
| influxdb-enterprise-active.imagePullSecrets | list | `[]` | List of pull secrets needed for images. If set, each object in the list should have one attribute, _name_, identifying the pull secret to use |
| influxdb-enterprise-active.license.key | string | `""` | License key. You can put your license key here for testing this chart out, but we STRONGLY recommend using a license file stored in a secret when you ship to production. |
| influxdb-enterprise-active.license.secret.key | string | `"json"` | Key within that secret that contains the license |
| influxdb-enterprise-active.license.secret.name | string | `"influxdb-enterprise-license"` | Name of the secret containing the license |
| influxdb-enterprise-active.meta.affinity | object | See `values.yaml` | Affinity rules for meta pods |
| influxdb-enterprise-active.meta.env | object | `{}` | Additional environment variables to set in the meta container |
| influxdb-enterprise-active.meta.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for meta images |
| influxdb-enterprise-active.meta.image.repository | string | `"influxdb"` | Docker repository for meta images |
| influxdb-enterprise-active.meta.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the meta ingress |
| influxdb-enterprise-active.meta.ingress.className | string | `"nginx"` | Ingress class name of the meta service |
| influxdb-enterprise-active.meta.ingress.enabled | bool | `false` | Whether to enable an ingress for the meta service |
| influxdb-enterprise-active.meta.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the meta ingress |
| influxdb-enterprise-active.meta.ingress.path | string | `"/influxdb-enterprise-meta(/\|$)(.*)"` | Path of the meta service |
| influxdb-enterprise-active.meta.nodeSelector | object | `{}` | Node selection rules for meta pods |
| influxdb-enterprise-active.meta.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for the persistent volume claim |
| influxdb-enterprise-active.meta.persistence.annotations | object | `{}` | Annotations to add to the persistent volume claim |
| influxdb-enterprise-active.meta.persistence.enabled | bool | `false` | Whether to persist data to a persistent volume |
| influxdb-enterprise-active.meta.persistence.existingClaim | string | Use a volume claim template | Manually managed PersistentVolumeClaim to use. If defined, this PVC must be created manually before the meta service will start |
| influxdb-enterprise-active.meta.persistence.size | string | `"8Gi"` | Size of persistent volume to request |
| influxdb-enterprise-active.meta.persistence.storageClass | string | `""` | Storage class of the persistent volume (set to `-` to disable dynamic provisioning, leave unset to use the default provisioner |
| influxdb-enterprise-active.meta.podAnnotations | object | `{}` | Annotations for meta pods |
| influxdb-enterprise-active.meta.podDisruptionBudget.minAvailable | int | `2` | Minimum available pods to maintain |
| influxdb-enterprise-active.meta.podSecurityContext | object | `{}` | Pod security context for meta pods |
| influxdb-enterprise-active.meta.preruncmds | list | `[]` | Commands to run in meta pods before InfluxDB is started. Each list entry should have a _cmd_ key with the command to run and an optional _description_ key describing that command |
| influxdb-enterprise-active.meta.replicas | int | `3` | Number of meta pods to run |
| influxdb-enterprise-active.meta.resources | object | `{}` | Kubernetes resources and limits for the meta container |
| influxdb-enterprise-active.meta.securityContext | object | `{}` | Security context for meta pods |
| influxdb-enterprise-active.meta.service.annotations | object | `{}` | Extra annotations for the meta service |
| influxdb-enterprise-active.meta.service.externalIPs | list | Do not allocate external IPs | External IPs for the meta service |
| influxdb-enterprise-active.meta.service.externalTrafficPolicy | string | Do not set an external traffic policy | External traffic policy for the meta service |
| influxdb-enterprise-active.meta.service.loadBalancerIP | string | Do not allocate a load balancer IP | Load balancer IP for the meta service |
| influxdb-enterprise-active.meta.service.nodePort | int | Do not allocate a node port | Node port for the meta service |
| influxdb-enterprise-active.meta.service.type | string | `"ClusterIP"` | Service type for the meta service |
| influxdb-enterprise-active.meta.sharedSecret.secret | object | `{"key":"secret","name":"influxdb-enterprise-shared-secret"}` | Shared secret used by the internal API for JWT authentication between InfluxDB nodes. Must have a key named `secret` that should be a long, random string See [documentation for shared-internal-secret](https://docs.influxdata.com/enterprise_influxdb/v1/administration/configure/config-data-nodes/#meta-internal-shared-secret). |
| influxdb-enterprise-active.meta.sharedSecret.secret.key | string | `"secret"` | Key within that secret that contains the shared secret |
| influxdb-enterprise-active.meta.sharedSecret.secret.name | string | `"influxdb-enterprise-shared-secret"` | Name of the secret containing the shared secret |
| influxdb-enterprise-active.meta.tolerations | list | `[]` | Tolerations for meta pods |
| influxdb-enterprise-active.nameOverride | string | `""` | Override the base name for resources |
| influxdb-enterprise-active.serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| influxdb-enterprise-active.serviceAccount.create | bool | `false` | Whether to create a Kubernetes service account to run as |
| influxdb-enterprise-active.serviceAccount.name | string | Name based on the chart fullname | Name of the Kubernetes service account to run as |
| influxdb-enterprise-standby.bootstrap.auth.secretName | string | `"sasquatch"` | Enable authentication of the data nodes using this secret, by creating a username and password for an admin account. The secret must contain keys `username` and `password`. |
| influxdb-enterprise-standby.bootstrap.ddldml.configMap | string | Do not run DDL or DML | A config map containing DDL and DML that define databases, retention policies, and inject some data.  The keys `ddl` and `dml` must exist, even if one of them is empty.  DDL is executed before DML to ensure databases and retention policies exist. |
| influxdb-enterprise-standby.bootstrap.ddldml.resources | object | `{}` | Kubernetes resources and limits for the bootstrap job |
| influxdb-enterprise-standby.data.affinity | object | See `values.yaml` | Affinity rules for data pods |
| influxdb-enterprise-standby.data.config.antiEntropy.enabled | bool | `false` | Enable the anti-entropy service, which copies and repairs shards |
| influxdb-enterprise-standby.data.config.cluster.log-queries-after | string | `"15s"` | Maximum duration a query can run before InfluxDB logs it as a slow query |
| influxdb-enterprise-standby.data.config.cluster.max-concurrent-queries | int | `1000` | Maximum number of running queries allowed on the instance (0 is unlimited) |
| influxdb-enterprise-standby.data.config.cluster.query-timeout | string | `"300s"` | Maximum duration a query is allowed to run before it is killed |
| influxdb-enterprise-standby.data.config.continuousQueries.enabled | bool | `false` | Whether continuous queries are enabled |
| influxdb-enterprise-standby.data.config.data.cache-max-memory-size | int | `0` | Maximum size a shared cache can reach before it starts rejecting writes |
| influxdb-enterprise-standby.data.config.data.trace-logging-enabled | bool | `true` | Whether to enable verbose logging of additional debug information within the TSM engine and WAL |
| influxdb-enterprise-standby.data.config.data.wal-fsync-delay | string | `"100ms"` | Duration a write will wait before fsyncing. This is useful for slower disks or when WAL write contention is present. |
| influxdb-enterprise-standby.data.config.hintedHandoff.max-size | int | `107374182400` | Maximum size of the hinted-handoff queue in bytes |
| influxdb-enterprise-standby.data.config.http.auth-enabled | bool | `true` | Whether authentication is required |
| influxdb-enterprise-standby.data.config.http.flux-enabled | bool | `true` | Whether to enable the Flux query endpoint |
| influxdb-enterprise-standby.data.config.logging.level | string | `"debug"` | Logging level |
| influxdb-enterprise-standby.data.env | object | `{}` | Additional environment variables to set in the meta container |
| influxdb-enterprise-standby.data.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for data images |
| influxdb-enterprise-standby.data.image.repository | string | `"influxdb"` | Docker repository for data images |
| influxdb-enterprise-standby.data.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the data ingress |
| influxdb-enterprise-standby.data.ingress.className | string | `"nginx"` | Ingress class name of the data service |
| influxdb-enterprise-standby.data.ingress.enabled | bool | `false` | Whether to enable an ingress for the data service |
| influxdb-enterprise-standby.data.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the data ingress |
| influxdb-enterprise-standby.data.ingress.path | string | `"/influxdb-enterprise-data(/\|$)(.*)"` | Path of the data service |
| influxdb-enterprise-standby.data.nodeSelector | object | `{}` | Node selection rules for data pods |
| influxdb-enterprise-standby.data.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for the persistent volume claim |
| influxdb-enterprise-standby.data.persistence.annotations | object | `{}` | Annotations to add to the persistent volume claim |
| influxdb-enterprise-standby.data.persistence.enabled | bool | `false` | Whether to persist data to a persistent volume |
| influxdb-enterprise-standby.data.persistence.existingClaim | string | Use a volume claim template | Manually managed PersistentVolumeClaim to use. If defined, this PVC must be created manually before the meta service will start |
| influxdb-enterprise-standby.data.persistence.size | string | `"8Gi"` | Size of persistent volume to request |
| influxdb-enterprise-standby.data.persistence.storageClass | string | `""` | Storage class of the persistent volume (set to `-` to disable dynamic provisioning, leave unset to use the default provisioner |
| influxdb-enterprise-standby.data.podAnnotations | object | `{}` | Annotations for data pods |
| influxdb-enterprise-standby.data.podDisruptionBudget.minAvailable | int | `1` | Minimum available pods to maintain |
| influxdb-enterprise-standby.data.podSecurityContext | object | `{}` | Pod security context for data pods |
| influxdb-enterprise-standby.data.preruncmds | list | `[]` | Commands to run in data pods before InfluxDB is started. Each list entry should have a _cmd_ key with the command to run and an optional _description_ key describing that command |
| influxdb-enterprise-standby.data.replicas | int | `1` | Number of data replicas to run |
| influxdb-enterprise-standby.data.resources | object | `{}` | Kubernetes resources and limits for the meta container |
| influxdb-enterprise-standby.data.securityContext | object | `{}` | Security context for meta pods |
| influxdb-enterprise-standby.data.service.annotations | object | `{}` | Extra annotations for the data service |
| influxdb-enterprise-standby.data.service.externalIPs | list | Do not allocate external IPs | External IPs for the data service |
| influxdb-enterprise-standby.data.service.externalTrafficPolicy | string | Do not set an external traffic policy | External traffic policy for the data service |
| influxdb-enterprise-standby.data.service.loadBalancerIP | string | Do not allocate a load balancer IP | Load balancer IP for the data service |
| influxdb-enterprise-standby.data.service.nodePort | int | Do not allocate a node port | Node port for the data service |
| influxdb-enterprise-standby.data.service.type | string | `"ClusterIP"` | Service type for the data service |
| influxdb-enterprise-standby.data.tolerations | list | `[]` | Tolerations for data pods |
| influxdb-enterprise-standby.envFromSecret | string | No secret | The name of a secret in the same kubernetes namespace which contain values to be added to the environment |
| influxdb-enterprise-standby.fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| influxdb-enterprise-standby.image.addsuffix | bool | `false` | Set to true to add a suffix for the type of image to the Docker tag (for example, `-meta`, making an image name of `influxdb:1.8.0-meta`) |
| influxdb-enterprise-standby.image.tag | string | `appVersion` from `Chart.yaml` | Tagged version of the Docker image that you want to run |
| influxdb-enterprise-standby.imagePullSecrets | list | `[]` | List of pull secrets needed for images. If set, each object in the list should have one attribute, _name_, identifying the pull secret to use |
| influxdb-enterprise-standby.license.key | string | `""` | License key. You can put your license key here for testing this chart out, but we STRONGLY recommend using a license file stored in a secret when you ship to production. |
| influxdb-enterprise-standby.license.secret.key | string | `"json"` | Key within that secret that contains the license |
| influxdb-enterprise-standby.license.secret.name | string | `"influxdb-enterprise-license"` | Name of the secret containing the license |
| influxdb-enterprise-standby.meta.affinity | object | See `values.yaml` | Affinity rules for meta pods |
| influxdb-enterprise-standby.meta.env | object | `{}` | Additional environment variables to set in the meta container |
| influxdb-enterprise-standby.meta.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for meta images |
| influxdb-enterprise-standby.meta.image.repository | string | `"influxdb"` | Docker repository for meta images |
| influxdb-enterprise-standby.meta.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the meta ingress |
| influxdb-enterprise-standby.meta.ingress.className | string | `"nginx"` | Ingress class name of the meta service |
| influxdb-enterprise-standby.meta.ingress.enabled | bool | `false` | Whether to enable an ingress for the meta service |
| influxdb-enterprise-standby.meta.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the meta ingress |
| influxdb-enterprise-standby.meta.ingress.path | string | `"/influxdb-enterprise-meta(/\|$)(.*)"` | Path of the meta service |
| influxdb-enterprise-standby.meta.nodeSelector | object | `{}` | Node selection rules for meta pods |
| influxdb-enterprise-standby.meta.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for the persistent volume claim |
| influxdb-enterprise-standby.meta.persistence.annotations | object | `{}` | Annotations to add to the persistent volume claim |
| influxdb-enterprise-standby.meta.persistence.enabled | bool | `false` | Whether to persist data to a persistent volume |
| influxdb-enterprise-standby.meta.persistence.existingClaim | string | Use a volume claim template | Manually managed PersistentVolumeClaim to use. If defined, this PVC must be created manually before the meta service will start |
| influxdb-enterprise-standby.meta.persistence.size | string | `"8Gi"` | Size of persistent volume to request |
| influxdb-enterprise-standby.meta.persistence.storageClass | string | `""` | Storage class of the persistent volume (set to `-` to disable dynamic provisioning, leave unset to use the default provisioner |
| influxdb-enterprise-standby.meta.podAnnotations | object | `{}` | Annotations for meta pods |
| influxdb-enterprise-standby.meta.podDisruptionBudget.minAvailable | int | `2` | Minimum available pods to maintain |
| influxdb-enterprise-standby.meta.podSecurityContext | object | `{}` | Pod security context for meta pods |
| influxdb-enterprise-standby.meta.preruncmds | list | `[]` | Commands to run in meta pods before InfluxDB is started. Each list entry should have a _cmd_ key with the command to run and an optional _description_ key describing that command |
| influxdb-enterprise-standby.meta.replicas | int | `3` | Number of meta pods to run |
| influxdb-enterprise-standby.meta.resources | object | `{}` | Kubernetes resources and limits for the meta container |
| influxdb-enterprise-standby.meta.securityContext | object | `{}` | Security context for meta pods |
| influxdb-enterprise-standby.meta.service.annotations | object | `{}` | Extra annotations for the meta service |
| influxdb-enterprise-standby.meta.service.externalIPs | list | Do not allocate external IPs | External IPs for the meta service |
| influxdb-enterprise-standby.meta.service.externalTrafficPolicy | string | Do not set an external traffic policy | External traffic policy for the meta service |
| influxdb-enterprise-standby.meta.service.loadBalancerIP | string | Do not allocate a load balancer IP | Load balancer IP for the meta service |
| influxdb-enterprise-standby.meta.service.nodePort | int | Do not allocate a node port | Node port for the meta service |
| influxdb-enterprise-standby.meta.service.type | string | `"ClusterIP"` | Service type for the meta service |
| influxdb-enterprise-standby.meta.sharedSecret.secret | object | `{"key":"secret","name":"influxdb-enterprise-shared-secret"}` | Shared secret used by the internal API for JWT authentication between InfluxDB nodes. Must have a key named `secret` that should be a long, random string See [documentation for shared-internal-secret](https://docs.influxdata.com/enterprise_influxdb/v1/administration/configure/config-data-nodes/#meta-internal-shared-secret). |
| influxdb-enterprise-standby.meta.sharedSecret.secret.key | string | `"secret"` | Key within that secret that contains the shared secret |
| influxdb-enterprise-standby.meta.sharedSecret.secret.name | string | `"influxdb-enterprise-shared-secret"` | Name of the secret containing the shared secret |
| influxdb-enterprise-standby.meta.tolerations | list | `[]` | Tolerations for meta pods |
| influxdb-enterprise-standby.nameOverride | string | `""` | Override the base name for resources |
| influxdb-enterprise-standby.serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| influxdb-enterprise-standby.serviceAccount.create | bool | `false` | Whether to create a Kubernetes service account to run as |
| influxdb-enterprise-standby.serviceAccount.name | string | Name based on the chart fullname | Name of the Kubernetes service account to run as |
| kafdrop.affinity | object | `{}` | Affinity configuration |
| kafdrop.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| kafdrop.cmdArgs | string | See `values.yaml` | Command line arguments to Kafdrop |
| kafdrop.existingSecret | string | Do not use a secret | Existing Kubernetes secrect use to set kafdrop environment variables. Set `SCHEMAREGISTRY_AUTH` for basic auth credentials in the form `<username>:<password>` |
| kafdrop.host | string | `"localhost"` | The hostname to report for the RMI registry (used for JMX) |
| kafdrop.image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| kafdrop.image.repository | string | `"obsidiandynamics/kafdrop"` | Kafdrop Docker image repository |
| kafdrop.image.tag | string | `"4.1.0"` | Kafdrop image version |
| kafdrop.ingress.annotations | object | `{}` | Additional ingress annotations |
| kafdrop.ingress.enabled | bool | `false` | Whether to enable the ingress |
| kafdrop.ingress.hostname | string | None, must be set if ingress is enabled | Ingress hostname |
| kafdrop.ingress.path | string | `"/kafdrop"` | Ingress path |
| kafdrop.jmx.port | int | `8686` | Port to use for JMX. If unspecified, JMX will not be exposed. |
| kafdrop.jvm.opts | string | `""` | JVM options |
| kafdrop.kafka.broker | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Bootstrap list of Kafka host/port pairs |
| kafdrop.nodeSelector | object | `{}` | Node selector configuration |
| kafdrop.podAnnotations | object | `{}` | Pod annotations |
| kafdrop.replicaCount | int | `1` | Number of kafdrop pods to run in the deployment. |
| kafdrop.resources | object | See `values.yaml` | Kubernetes requests and limits for Kafdrop |
| kafdrop.schemaregistry | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | The endpoint of Schema Registry |
| kafdrop.server.port | int | `9000` | The web server port to listen on |
| kafdrop.server.servlet.contextPath | string | `"/kafdrop"` | The context path to serve requests on |
| kafdrop.service.annotations | object | `{}` | Additional annotations to add to the service |
| kafdrop.service.port | int | `9000` | Service port |
| kafdrop.tolerations | list | `[]` | Tolerations configuration |
| kafka-connect-manager.cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations |
| kafka-connect-manager.enabled | bool | `false` | Whether to enable Kafka Connect Manager |
| kafka-connect-manager.env.kafkaBrokerUrl | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka broker URL |
| kafka-connect-manager.env.kafkaConnectUrl | string | `"http://sasquatch-connect-api.sasquatch:8083"` | Kafka connnect URL |
| kafka-connect-manager.env.kafkaUsername | string | `"kafka-connect-manager"` | Username for SASL authentication |
| kafka-connect-manager.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Kafka Connect Manager |
| kafka-connect-manager.image.repository | string | `"ghcr.io/lsst-sqre/kafkaconnect"` | Docker image to use for Kafka Connect Manager |
| kafka-connect-manager.image.tag | string | `"1.3.1"` | Docker tag to use for Kafka Connect Manager |
| kafka-connect-manager.influxdbSink.autoUpdate | bool | `true` | Whether to check for new Kafka topics |
| kafka-connect-manager.influxdbSink.checkInterval | string | `"15000"` | The interval, in milliseconds, to check for new topics and update the connector |
| kafka-connect-manager.influxdbSink.connectInfluxDb | string | `"efd"` | InfluxDB database to write to |
| kafka-connect-manager.influxdbSink.connectInfluxErrorPolicy | string | `"NOOP"` | Error policy, see connector documetation for details |
| kafka-connect-manager.influxdbSink.connectInfluxMaxRetries | string | `"10"` | The maximum number of times a message is retried |
| kafka-connect-manager.influxdbSink.connectInfluxRetryInterval | string | `"60000"` | The interval, in milliseconds, between retries. Only valid when the connectInfluxErrorPolicy is set to `RETRY`. |
| kafka-connect-manager.influxdbSink.connectInfluxUrl | string | `"http://sasquatch-influxdb.sasquatch:8086"` | InfluxDB URL |
| kafka-connect-manager.influxdbSink.connectProgressEnabled | bool | `false` | Enables the output for how many records have been processed |
| kafka-connect-manager.influxdbSink.connectors | object | See `values.yaml` | Connector instances to deploy. See `example` for the fields that can be set. |
| kafka-connect-manager.influxdbSink.excludedTopicsRegex | string | `""` | Regex to exclude topics from the list of selected topics from Kafka |
| kafka-connect-manager.influxdbSink.tasksMax | int | `1` | Maxium number of tasks to run the connector |
| kafka-connect-manager.influxdbSink.timestamp | string | `"private_efdStamp"` | Timestamp field to be used as the InfluxDB time. If not specified use `sys_time()`. |
| kafka-connect-manager.jdbcSink.autoCreate | string | `"true"` | Whether to automatically create the destination table |
| kafka-connect-manager.jdbcSink.autoEvolve | string | `"false"` | Whether to automatically add columns in the table schema |
| kafka-connect-manager.jdbcSink.batchSize | string | `"3000"` | Specifies how many records to attempt to batch together for insertion into the destination table |
| kafka-connect-manager.jdbcSink.connectionUrl | string | `"jdbc:postgresql://localhost:5432/mydb"` | Database connection URL |
| kafka-connect-manager.jdbcSink.dbTimezone | string | `"UTC"` | Name of the JDBC timezone that should be used in the connector when inserting time-based values |
| kafka-connect-manager.jdbcSink.enabled | bool | `false` | Whether the JDBC Sink connector is deployed |
| kafka-connect-manager.jdbcSink.insertMode | string | `"insert"` | The insertion mode to use. Supported modes are: `insert`, `upsert` and `update`. |
| kafka-connect-manager.jdbcSink.maxRetries | string | `"10"` | The maximum number of times to retry on errors before failing the task |
| kafka-connect-manager.jdbcSink.name | string | `"postgres-sink"` | Name of the connector to create |
| kafka-connect-manager.jdbcSink.retryBackoffMs | string | `"3000"` | The time in milliseconds to wait following an error before a retry attempt is made |
| kafka-connect-manager.jdbcSink.tableNameFormat | string | `"${topic}"` | A format string for the destination table name |
| kafka-connect-manager.jdbcSink.tasksMax | string | `"10"` | Number of Kafka Connect tasks |
| kafka-connect-manager.jdbcSink.topicRegex | string | `".*"` | Regex for selecting topics |
| kafka-connect-manager.s3Sink.behaviorOnNullValues | string | `"fail"` | How to handle records with a null value (for example, Kafka tombstone records). Valid options are `ignore` and `fail`. |
| kafka-connect-manager.s3Sink.checkInterval | string | `"15000"` | The interval, in milliseconds, to check for new topics and update the connector |
| kafka-connect-manager.s3Sink.enabled | bool | `false` | Whether the Amazon S3 Sink connector is deployed |
| kafka-connect-manager.s3Sink.excludedTopicRegex | string | `""` | Regex to exclude topics from the list of selected topics from Kafka |
| kafka-connect-manager.s3Sink.flushSize | string | `"1000"` | Number of records written to store before invoking file commits |
| kafka-connect-manager.s3Sink.locale | string | `"en-US"` | The locale to use when partitioning with TimeBasedPartitioner |
| kafka-connect-manager.s3Sink.name | string | `"s3-sink"` | Name of the connector to create |
| kafka-connect-manager.s3Sink.partitionDurationMs | string | `"3600000"` | The duration of a partition in milliseconds, used by TimeBasedPartitioner. Default is 1h for an hourly based partitioner |
| kafka-connect-manager.s3Sink.pathFormat | string | `"'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH"` | Pattern used to format the path in the S3 object name |
| kafka-connect-manager.s3Sink.rotateIntervalMs | string | `"600000"` | The time interval in milliseconds to invoke file commits. Set to 10 minutes by default |
| kafka-connect-manager.s3Sink.s3BucketName | string | `""` | S3 bucket name. The bucket must already exist at the s3 provider |
| kafka-connect-manager.s3Sink.s3PartRetries | int | `3` | Maximum number of retry attempts for failed requests. Zero means no retries. |
| kafka-connect-manager.s3Sink.s3PartSize | int | `5242880` | The part size in S3 multi-part uploads. Valid values: [5242880,…,2147483647] |
| kafka-connect-manager.s3Sink.s3Region | string | `"us-east-1"` | S3 region |
| kafka-connect-manager.s3Sink.s3RetryBackoffMs | int | `200` | How long to wait in milliseconds before attempting the first retry of a failed S3 request |
| kafka-connect-manager.s3Sink.s3SchemaCompatibility | string | `"NONE"` | S3 schema compatibility |
| kafka-connect-manager.s3Sink.schemaCacheConfig | int | `5000` | The size of the schema cache used in the Avro converter |
| kafka-connect-manager.s3Sink.storeUrl | string | `""` | The object storage connection URL, for non-AWS s3 providers |
| kafka-connect-manager.s3Sink.tasksMax | int | `1` | Number of Kafka Connect tasks |
| kafka-connect-manager.s3Sink.timestampExtractor | string | `"Record"` | The extractor determines how to obtain a timestamp from each record |
| kafka-connect-manager.s3Sink.timestampField | string | `""` | The record field to be used as timestamp by the timestamp extractor. Only applies if timestampExtractor is set to RecordField. |
| kafka-connect-manager.s3Sink.timezone | string | `"UTC"` | The timezone to use when partitioning with TimeBasedPartitioner |
| kafka-connect-manager.s3Sink.topicsDir | string | `"topics"` | Top level directory to store the data ingested from Kafka |
| kafka-connect-manager.s3Sink.topicsRegex | string | `".*"` | Regex to select topics from Kafka |
| obsenv.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| obsloctap.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| prompt-processing.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| rest-proxy.affinity | object | `{}` | Affinity configuration |
| rest-proxy.configurationOverrides | object | See `values.yaml` | Kafka REST configuration options |
| rest-proxy.customEnv | object | `{}` | Kafka REST additional env variables |
| rest-proxy.heapOptions | string | `"-Xms512M -Xmx512M"` | Kafka REST proxy JVM Heap Option |
| rest-proxy.image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| rest-proxy.image.repository | string | `"confluentinc/cp-kafka-rest"` | Kafka REST proxy image repository |
| rest-proxy.image.tag | string | `"7.9.0"` | Kafka REST proxy image tag |
| rest-proxy.ingress.annotations | object | See `values.yaml` | Additional annotations to add to the ingress |
| rest-proxy.ingress.enabled | bool | `false` | Whether to enable the ingress |
| rest-proxy.ingress.hostname | string | None, must be set if ingress is enabled | Ingress hostname |
| rest-proxy.ingress.path | string | `"/sasquatch-rest-proxy(/|$)(.*)"` | Ingress path @default - `"/sasquatch-rest-proxy(/\|$)(.*)"` |
| rest-proxy.kafka.bootstrapServers | string | `"SASL_PLAINTEXT://sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka bootstrap servers, use the internal listerner on port 9092 with SASL connection |
| rest-proxy.kafka.cluster.name | string | `"sasquatch"` | Name of the Strimzi Kafka cluster. |
| rest-proxy.kafka.topicPrefixes | list | `[]` | List of topic prefixes to use when exposing Kafka topics to the REST Proxy v2 API. |
| rest-proxy.kafka.topics | list | `[]` | List of Kafka topics to create via Strimzi. Alternatively topics can be created using the REST Proxy v3 API. |
| rest-proxy.nodeSelector | object | `{}` | Node selector configuration |
| rest-proxy.podAnnotations | object | `{}` | Pod annotations |
| rest-proxy.replicaCount | int | `3` | Number of Kafka REST proxy pods to run in the deployment |
| rest-proxy.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka REST proxy |
| rest-proxy.schemaregistry.url | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Schema registry URL |
| rest-proxy.service.port | int | `8082` | Kafka REST proxy service port |
| rest-proxy.tolerations | list | `[]` | Tolerations configuration |
| square-events.cluster.name | string | `"sasquatch"` |  |
| strimzi-kafka.brokerStorage | object | `{"enabled":false,"migration":{"brokers":[0,1,2],"enabled":false,"rebalance":false},"size":"1.5Ti","storageClassName":"localdrive"}` | Configuration for deploying Kafka brokers with local storage |
| strimzi-kafka.cluster.monitorLabel | object | `{}` | Site wide label required for gathering Prometheus metrics if they are enabled |
| strimzi-kafka.cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations |
| strimzi-kafka.connect.config."key.converter" | string | `"io.confluent.connect.avro.AvroConverter"` | Set the converter for the message ke |
| strimzi-kafka.connect.config."key.converter.schema.registry.url" | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | URL for the schema registry |
| strimzi-kafka.connect.config."key.converter.schemas.enable" | bool | `true` | Enable converted schemas for the message key |
| strimzi-kafka.connect.config."value.converter" | string | `"io.confluent.connect.avro.AvroConverter"` | Converter for the message value |
| strimzi-kafka.connect.config."value.converter.schema.registry.url" | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | URL for the schema registry |
| strimzi-kafka.connect.config."value.converter.schemas.enable" | bool | `true` | Enable converted schemas for the message value |
| strimzi-kafka.connect.enabled | bool | `false` | Enable Kafka Connect |
| strimzi-kafka.connect.image | string | `"ghcr.io/lsst-sqre/strimzi-0.40.0-kafka-3.7.0:tickets-DM-43491"` | Custom strimzi-kafka image with connector plugins used by sasquatch |
| strimzi-kafka.connect.replicas | int | `3` | Number of Kafka Connect replicas to run |
| strimzi-kafka.cruiseControl | object | `{"enabled":false}` | Configuration for the Kafka Cruise Control |
| strimzi-kafka.kafka.affinity | object | See `values.yaml` | Affinity for Kafka pod assignment |
| strimzi-kafka.kafka.config."log.retention.minutes" | int | 4320 minutes (3 days) | Number of days for a topic's data to be retained |
| strimzi-kafka.kafka.config."message.max.bytes" | int | `10485760` | The largest record batch size allowed by Kafka |
| strimzi-kafka.kafka.config."offsets.retention.minutes" | int | 4320 minutes (3 days) | Number of minutes for a consumer group's offsets to be retained |
| strimzi-kafka.kafka.config."replica.fetch.max.bytes" | int | `10485760` | The number of bytes of messages to attempt to fetch for each partition |
| strimzi-kafka.kafka.externalListener.bootstrap.annotations | object | `{}` | Annotations that will be added to the Ingress, Route, or Service resource |
| strimzi-kafka.kafka.externalListener.bootstrap.host | string | Do not configure TLS | Name used for TLS hostname verification |
| strimzi-kafka.kafka.externalListener.bootstrap.loadBalancerIP | string | Do not request a load balancer IP | Request this load balancer IP. See `values.yaml` for more discussion |
| strimzi-kafka.kafka.externalListener.brokers | list | `[]` | Brokers configuration. _host_ is used in the brokers' advertised.brokers configuration and for TLS hostname verification.  The format is a list of maps. |
| strimzi-kafka.kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker |
| strimzi-kafka.kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled |
| strimzi-kafka.kafka.listeners.external.enabled | bool | `false` | Whether external listener is enabled |
| strimzi-kafka.kafka.listeners.plain.enabled | bool | `false` | Whether internal plaintext listener is enabled |
| strimzi-kafka.kafka.listeners.tls.enabled | bool | `false` | Whether internal TLS listener is enabled |
| strimzi-kafka.kafka.metricsConfig.enabled | bool | `false` | Whether metric configuration is enabled |
| strimzi-kafka.kafka.minInsyncReplicas | int | `2` | The minimum number of in-sync replicas that must be available for the producer to successfully send records Cannot be greater than the number of replicas. |
| strimzi-kafka.kafka.replicas | int | `3` | Number of Kafka broker replicas to run |
| strimzi-kafka.kafka.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka brokers |
| strimzi-kafka.kafka.storage.size | string | `"500Gi"` | Size of the backing storage disk for each of the Kafka brokers |
| strimzi-kafka.kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes |
| strimzi-kafka.kafka.tolerations | list | `[]` | Tolerations for Kafka broker pod assignment |
| strimzi-kafka.kafka.version | string | `"3.8.0"` | Version of Kafka to deploy |
| strimzi-kafka.kafkaController.enabled | bool | `false` | Enable Kafka Controller |
| strimzi-kafka.kafkaController.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka Controller |
| strimzi-kafka.kafkaController.storage.size | string | `"20Gi"` | Size of the backing storage disk for each of the Kafka controllers |
| strimzi-kafka.kafkaController.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes |
| strimzi-kafka.kafkaExporter.enableSaramaLogging | bool | `false` | Enable Sarama logging for pod |
| strimzi-kafka.kafkaExporter.enabled | bool | `false` | Enable Kafka exporter |
| strimzi-kafka.kafkaExporter.groupRegex | string | `".*"` | Consumer groups to monitor |
| strimzi-kafka.kafkaExporter.logging | string | `"info"` | Logging level |
| strimzi-kafka.kafkaExporter.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka exporter |
| strimzi-kafka.kafkaExporter.topicRegex | string | `".*"` | Kafka topics to monitor |
| strimzi-kafka.kraft.enabled | bool | `false` | Enable KRaft mode for Kafka |
| strimzi-kafka.mirrormaker2.enabled | bool | `false` | Enable replication in the target (passive) cluster |
| strimzi-kafka.mirrormaker2.replicas | int | `3` | Number of Mirror Maker replicas to run |
| strimzi-kafka.mirrormaker2.replication.policy.class | string | `"org.apache.kafka.connect.mirror.IdentityReplicationPolicy"` | Replication policy. |
| strimzi-kafka.mirrormaker2.replication.policy.separator | string | `""` | Convention used to rename topics when the DefaultReplicationPolicy replication policy is used. Default is "" when the IdentityReplicationPolicy replication policy is used. |
| strimzi-kafka.mirrormaker2.source.bootstrapServer | string | None, must be set if enabled | Source (active) cluster to replicate from |
| strimzi-kafka.mirrormaker2.source.topicsPattern | string | `"registry-schemas, lsst.sal.*"` | Topic replication from the source cluster defined as a comma-separated list or regular expression pattern |
| strimzi-kafka.registry.ingress.annotations | object | `{}` | Annotations that will be added to the Ingress resource |
| strimzi-kafka.registry.ingress.enabled | bool | `false` | Whether to enable an ingress for the Schema Registry |
| strimzi-kafka.registry.ingress.hostname | string | None, must be set if ingress is enabled | Hostname for the Schema Registry |
| strimzi-kafka.registry.resources | object | See `values.yaml` | Kubernetes requests and limits for the Schema Registry |
| strimzi-kafka.registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| strimzi-kafka.superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| strimzi-kafka.users.replicator.enabled | bool | `false` | Enable user replicator (used by Mirror Maker 2 and required at both source and target clusters) |
| strimzi-kafka.users.telegraf.enabled | bool | `false` | Enable user telegraf (deployed by parent Sasquatch chart) |
| tap.cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| telegraf.affinity | object | `{}` | Affinity for pod assignment |
| telegraf.args | list | `[]` | Arguments passed to the Telegraf agent on startup |
| telegraf.enabled | bool | `false` | Wether Telegraf is enabled |
| telegraf.env | list | See `values.yaml` | Telegraf agent environment variables |
| telegraf.envFromSecret | string | `""` | Name of the secret with values to be added to the environment. |
| telegraf.image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| telegraf.image.repo | string | `"docker.io/library/telegraf"` | Telegraf image repository |
| telegraf.image.tag | string | `"1.32.1-alpine"` | Telegraf image tag |
| telegraf.imagePullSecrets | list | `[]` | Secret names to use for Docker pulls |
| telegraf.influxdb.url | string | `"http://sasquatch-influxdb.sasquatch:8086"` | URL of the InfluxDB v1 instance to write to |
| telegraf.kafkaConsumers.test.collection_jitter | string | "0s" | Data collection jitter. This is used to jitter the collection by a random amount. Each plugin will sleep for a random time within jitter before collecting. |
| telegraf.kafkaConsumers.test.compression_codec | int | 3 | Compression codec. 0 : None, 1 : Gzip, 2 : Snappy, 3 : LZ4, 4 : ZSTD |
| telegraf.kafkaConsumers.test.consumer_fetch_default | string | "20MB" | Maximum amount of data the server should return for a fetch request. |
| telegraf.kafkaConsumers.test.database | string | `""` | Name of the InfluxDB v1 database to write to (required) |
| telegraf.kafkaConsumers.test.debug | bool | false | Run Telegraf in debug mode. |
| telegraf.kafkaConsumers.test.enabled | bool | `false` | Enable the Telegraf Kafka consumer. |
| telegraf.kafkaConsumers.test.fields | list | `[]` | List of Avro fields to be recorded as InfluxDB fields.  If not specified, any Avro field that is not marked as a tag will become an InfluxDB field. |
| telegraf.kafkaConsumers.test.flush_interval | string | "10s" | Data flushing interval for all outputs. Don’t set this below interval. Maximum flush_interval is flush_interval + flush_jitter |
| telegraf.kafkaConsumers.test.flush_jitter | string | "0s" | Jitter the flush interval by a random amount. This is primarily to avoid large write spikes for users running a large number of telegraf instances. |
| telegraf.kafkaConsumers.test.max_processing_time | string | "5s" | Maximum processing time for a single message. |
| telegraf.kafkaConsumers.test.max_undelivered_messages | int | 10000 | Maximum number of undelivered messages. Should be a multiple of metric_batch_size, setting it too low may never flush the broker's messages. |
| telegraf.kafkaConsumers.test.metric_batch_size | int | 1000 | Sends metrics to the output in batches of at most metric_batch_size metrics. |
| telegraf.kafkaConsumers.test.metric_buffer_limit | int | 100000 | Caches metric_buffer_limit metrics for each output, and flushes this buffer on a successful write. This should be a multiple of metric_batch_size and could not be less than 2 times metric_batch_size. |
| telegraf.kafkaConsumers.test.offset | string | `"oldest"` | Kafka consumer offset. Possible values are `oldest` and `newest`. |
| telegraf.kafkaConsumers.test.precision | string | "1us" | Data precision. |
| telegraf.kafkaConsumers.test.replicaCount | int | `1` | Number of Telegraf Kafka consumer replicas. Increase this value to increase the consumer throughput. |
| telegraf.kafkaConsumers.test.tags | list | `[]` | List of Avro fields to be recorded as InfluxDB tags.  The Avro fields specified as tags will be converted to strings before ingestion into InfluxDB. |
| telegraf.kafkaConsumers.test.timestamp_field | string | `"private_efdStamp"` | Avro field to be used as the InfluxDB timestamp (optional).  If unspecified or set to the empty string, Telegraf will use the time it received the measurement. |
| telegraf.kafkaConsumers.test.timestamp_format | string | `"unix"` | Timestamp format. Possible values are `unix` (the default if unset) a timestamp in seconds since the Unix epoch, `unix_ms` (milliseconds), `unix_us` (microsseconds), or `unix_ns` (nanoseconds). |
| telegraf.kafkaConsumers.test.topicRegexps | string | `"[ \".*Test\" ]\n"` | List of regular expressions to specify the Kafka topics consumed by this agent. |
| telegraf.kafkaConsumers.test.union_field_separator | string | `""` | Union field separator: if a single Avro field is flattened into more than one InfluxDB field (e.g. an array `a`, with four members, would yield `a0`, `a1`, `a2`, `a3`; if the field separator were `_`, these would be `a_0`...`a_3`. |
| telegraf.kafkaConsumers.test.union_mode | string | `"nullable"` | Union mode: this can be one of `flatten`, `nullable`, or `any`. See `values.yaml` for extensive discussion. |
| telegraf.nodeSelector | object | `{}` | Node labels for pod assignment |
| telegraf.podAnnotations | object | `{}` | Annotations for the Telegraf pods |
| telegraf.podLabels | object | `{}` | Labels for the Telegraf pods |
| telegraf.resources | object | See `values.yaml` | Kubernetes resources requests and limits |
| telegraf.tolerations | list | `[]` | Tolerations for pod assignment |
| telegraf-oss.affinity | object | `{}` | Affinity for pod assignment |
| telegraf-oss.args | list | `[]` | Arguments passed to the Telegraf agent on startup |
| telegraf-oss.enabled | bool | `false` | Wether Telegraf is enabled |
| telegraf-oss.env | list | See `values.yaml` | Telegraf agent environment variables |
| telegraf-oss.envFromSecret | string | `""` | Name of the secret with values to be added to the environment. |
| telegraf-oss.image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| telegraf-oss.image.repo | string | `"docker.io/library/telegraf"` | Telegraf image repository |
| telegraf-oss.image.tag | string | `"1.32.1-alpine"` | Telegraf image tag |
| telegraf-oss.imagePullSecrets | list | `[]` | Secret names to use for Docker pulls |
| telegraf-oss.influxdb.url | string | `"http://sasquatch-influxdb.sasquatch:8086"` | URL of the InfluxDB v1 instance to write to |
| telegraf-oss.kafkaConsumers.test.collection_jitter | string | "0s" | Data collection jitter. This is used to jitter the collection by a random amount. Each plugin will sleep for a random time within jitter before collecting. |
| telegraf-oss.kafkaConsumers.test.compression_codec | int | 3 | Compression codec. 0 : None, 1 : Gzip, 2 : Snappy, 3 : LZ4, 4 : ZSTD |
| telegraf-oss.kafkaConsumers.test.consumer_fetch_default | string | "20MB" | Maximum amount of data the server should return for a fetch request. |
| telegraf-oss.kafkaConsumers.test.database | string | `""` | Name of the InfluxDB v1 database to write to (required) |
| telegraf-oss.kafkaConsumers.test.debug | bool | false | Run Telegraf in debug mode. |
| telegraf-oss.kafkaConsumers.test.enabled | bool | `false` | Enable the Telegraf Kafka consumer. |
| telegraf-oss.kafkaConsumers.test.fields | list | `[]` | List of Avro fields to be recorded as InfluxDB fields.  If not specified, any Avro field that is not marked as a tag will become an InfluxDB field. |
| telegraf-oss.kafkaConsumers.test.flush_interval | string | "10s" | Data flushing interval for all outputs. Don’t set this below interval. Maximum flush_interval is flush_interval + flush_jitter |
| telegraf-oss.kafkaConsumers.test.flush_jitter | string | "0s" | Jitter the flush interval by a random amount. This is primarily to avoid large write spikes for users running a large number of telegraf instances. |
| telegraf-oss.kafkaConsumers.test.max_processing_time | string | "5s" | Maximum processing time for a single message. |
| telegraf-oss.kafkaConsumers.test.max_undelivered_messages | int | 10000 | Maximum number of undelivered messages. Should be a multiple of metric_batch_size, setting it too low may never flush the broker's messages. |
| telegraf-oss.kafkaConsumers.test.metric_batch_size | int | 1000 | Sends metrics to the output in batches of at most metric_batch_size metrics. |
| telegraf-oss.kafkaConsumers.test.metric_buffer_limit | int | 100000 | Caches metric_buffer_limit metrics for each output, and flushes this buffer on a successful write. This should be a multiple of metric_batch_size and could not be less than 2 times metric_batch_size. |
| telegraf-oss.kafkaConsumers.test.offset | string | `"oldest"` | Kafka consumer offset. Possible values are `oldest` and `newest`. |
| telegraf-oss.kafkaConsumers.test.precision | string | "1us" | Data precision. |
| telegraf-oss.kafkaConsumers.test.replicaCount | int | `1` | Number of Telegraf Kafka consumer replicas. Increase this value to increase the consumer throughput. |
| telegraf-oss.kafkaConsumers.test.tags | list | `[]` | List of Avro fields to be recorded as InfluxDB tags.  The Avro fields specified as tags will be converted to strings before ingestion into InfluxDB. |
| telegraf-oss.kafkaConsumers.test.timestamp_field | string | `"private_efdStamp"` | Avro field to be used as the InfluxDB timestamp (optional).  If unspecified or set to the empty string, Telegraf will use the time it received the measurement. |
| telegraf-oss.kafkaConsumers.test.timestamp_format | string | `"unix"` | Timestamp format. Possible values are `unix` (the default if unset) a timestamp in seconds since the Unix epoch, `unix_ms` (milliseconds), `unix_us` (microsseconds), or `unix_ns` (nanoseconds). |
| telegraf-oss.kafkaConsumers.test.topicRegexps | string | `"[ \".*Test\" ]\n"` | List of regular expressions to specify the Kafka topics consumed by this agent. |
| telegraf-oss.kafkaConsumers.test.union_field_separator | string | `""` | Union field separator: if a single Avro field is flattened into more than one InfluxDB field (e.g. an array `a`, with four members, would yield `a0`, `a1`, `a2`, `a3`; if the field separator were `_`, these would be `a_0`...`a_3`. |
| telegraf-oss.kafkaConsumers.test.union_mode | string | `"nullable"` | Union mode: this can be one of `flatten`, `nullable`, or `any`. See `values.yaml` for extensive discussion. |
| telegraf-oss.nodeSelector | object | `{}` | Node labels for pod assignment |
| telegraf-oss.podAnnotations | object | `{}` | Annotations for the Telegraf pods |
| telegraf-oss.podLabels | object | `{}` | Labels for the Telegraf pods |
| telegraf-oss.resources | object | See `values.yaml` | Kubernetes resources requests and limits |
| telegraf-oss.tolerations | list | `[]` | Tolerations for pod assignment |
