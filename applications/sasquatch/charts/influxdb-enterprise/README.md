# influxdb-enterprise

Run InfluxDB Enterprise on Kubernetes

## Source Code

* <https://github.com/influxdata/influxdb>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| bootstrap.auth.secretName | string | `"sasquatch"` | Enable authentication of the data nodes using this secret, by creating a username and password for an admin account. The secret must contain keys `username` and `password`. |
| bootstrap.ddldml.configMap | string | Do not run DDL or DML | A config map containing DDL and DML that define databases, retention policies, and inject some data.  The keys `ddl` and `dml` must exist, even if one of them is empty.  DDL is executed before DML to ensure databases and retention policies exist. |
| bootstrap.ddldml.resources | object | `{}` | Kubernetes resources and limits for the bootstrap job |
| data.affinity | object | See `values.yaml` | Affinity rules for data pods |
| data.config.antiEntropy.enabled | bool | `false` | Enable the anti-entropy service, which copies and repairs shards |
| data.config.cluster.log-queries-after | string | `"15s"` | Maximum duration a query can run before InfluxDB logs it as a slow query |
| data.config.cluster.max-concurrent-queries | int | `1000` | Maximum number of running queries allowed on the instance (0 is unlimited) |
| data.config.cluster.query-timeout | string | `"300s"` | Maximum duration a query is allowed to run before it is killed |
| data.config.continuousQueries.enabled | bool | `false` | Whether continuous queries are enabled |
| data.config.data.cache-max-memory-size | int | `0` | Maximum size a shared cache can reach before it starts rejecting writes |
| data.config.data.trace-logging-enabled | bool | `true` | Whether to enable verbose logging of additional debug information within the TSM engine and WAL |
| data.config.data.wal-fsync-delay | string | `"100ms"` | Duration a write will wait before fsyncing. This is useful for slower disks or when WAL write contention is present. |
| data.config.hintedHandoff.max-size | int | `107374182400` | Maximum size of the hinted-handoff queue in bytes |
| data.config.http.auth-enabled | bool | `true` | Whether authentication is required |
| data.config.http.flux-enabled | bool | `true` | Whether to enable the Flux query endpoint |
| data.config.logging.level | string | `"debug"` | Logging level |
| data.env | object | `{}` | Additional environment variables to set in the meta container |
| data.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for data images |
| data.image.repository | string | `"influxdb"` | Docker repository for data images |
| data.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the data ingress |
| data.ingress.className | string | `"nginx"` | Ingress class name of the data service |
| data.ingress.enabled | bool | `false` | Whether to enable an ingress for the data service |
| data.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the data ingress |
| data.ingress.path | string | `"/influxdb-enterprise-data(/\|$)(.*)"` | Path of the data service |
| data.nodeSelector | object | `{}` | Node selection rules for data pods |
| data.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for the persistent volume claim |
| data.persistence.annotations | object | `{}` | Annotations to add to the persistent volume claim |
| data.persistence.enabled | bool | `false` | Whether to persist data to a persistent volume |
| data.persistence.existingClaim | string | Use a volume claim template | Manually managed PersistentVolumeClaim to use. If defined, this PVC must be created manually before the meta service will start |
| data.persistence.size | string | `"8Gi"` | Size of persistent volume to request |
| data.persistence.storageClass | string | `""` | Storage class of the persistent volume (set to `-` to disable dynamic provisioning, leave unset to use the default provisioner |
| data.podAnnotations | object | `{}` | Annotations for data pods |
| data.podDisruptionBudget.minAvailable | int | `1` | Minimum available pods to maintain |
| data.podSecurityContext | object | `{}` | Pod security context for data pods |
| data.preruncmds | list | `[]` | Commands to run in data pods before InfluxDB is started. Each list entry should have a _cmd_ key with the command to run and an optional _description_ key describing that command |
| data.replicas | int | `1` | Number of data replicas to run |
| data.resources | object | `{}` | Kubernetes resources and limits for the meta container |
| data.securityContext | object | `{}` | Security context for meta pods |
| data.service.annotations | object | `{}` | Extra annotations for the data service |
| data.service.externalIPs | list | Do not allocate external IPs | External IPs for the data service |
| data.service.externalTrafficPolicy | string | Do not set an external traffic policy | External traffic policy for the data service |
| data.service.loadBalancerIP | string | Do not allocate a load balancer IP | Load balancer IP for the data service |
| data.service.nodePort | int | Do not allocate a node port | Node port for the data service |
| data.service.type | string | `"ClusterIP"` | Service type for the data service |
| data.tolerations | list | `[]` | Tolerations for data pods |
| envFromSecret | string | No secret | The name of a secret in the same kubernetes namespace which contain values to be added to the environment |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| image.addsuffix | bool | `false` | Set to true to add a suffix for the type of image to the Docker tag (for example, `-meta`, making an image name of `influxdb:1.8.0-meta`) |
| image.tag | string | `appVersion` from `Chart.yaml` | Tagged version of the Docker image that you want to run |
| imagePullSecrets | list | `[]` | List of pull secrets needed for images. If set, each object in the list should have one attribute, _name_, identifying the pull secret to use |
| license.key | string | `""` | License key. You can put your license key here for testing this chart out, but we STRONGLY recommend using a license file stored in a secret when you ship to production. |
| license.secret.key | string | `"json"` | Key within that secret that contains the license |
| license.secret.name | string | `"influxdb-enterprise-license"` | Name of the secret containing the license |
| meta.affinity | object | See `values.yaml` | Affinity rules for meta pods |
| meta.env | object | `{}` | Additional environment variables to set in the meta container |
| meta.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for meta images |
| meta.image.repository | string | `"influxdb"` | Docker repository for meta images |
| meta.ingress.annotations | object | See `values.yaml` | Extra annotations to add to the meta ingress |
| meta.ingress.className | string | `"nginx"` | Ingress class name of the meta service |
| meta.ingress.enabled | bool | `false` | Whether to enable an ingress for the meta service |
| meta.ingress.hostname | string | None, must be set if the ingress is enabled | Hostname of the meta ingress |
| meta.ingress.path | string | `"/influxdb-enterprise-meta(/\|$)(.*)"` | Path of the meta service |
| meta.nodeSelector | object | `{}` | Node selection rules for meta pods |
| meta.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode for the persistent volume claim |
| meta.persistence.annotations | object | `{}` | Annotations to add to the persistent volume claim |
| meta.persistence.enabled | bool | `false` | Whether to persist data to a persistent volume |
| meta.persistence.existingClaim | string | Use a volume claim template | Manually managed PersistentVolumeClaim to use. If defined, this PVC must be created manually before the meta service will start |
| meta.persistence.size | string | `"8Gi"` | Size of persistent volume to request |
| meta.persistence.storageClass | string | `""` | Storage class of the persistent volume (set to `-` to disable dynamic provisioning, leave unset to use the default provisioner |
| meta.podAnnotations | object | `{}` | Annotations for meta pods |
| meta.podDisruptionBudget.minAvailable | int | `2` | Minimum available pods to maintain |
| meta.podSecurityContext | object | `{}` | Pod security context for meta pods |
| meta.preruncmds | list | `[]` | Commands to run in meta pods before InfluxDB is started. Each list entry should have a _cmd_ key with the command to run and an optional _description_ key describing that command |
| meta.replicas | int | `3` | Number of meta pods to run |
| meta.resources | object | `{}` | Kubernetes resources and limits for the meta container |
| meta.securityContext | object | `{}` | Security context for meta pods |
| meta.service.annotations | object | `{}` | Extra annotations for the meta service |
| meta.service.externalIPs | list | Do not allocate external IPs | External IPs for the meta service |
| meta.service.externalTrafficPolicy | string | Do not set an external traffic policy | External traffic policy for the meta service |
| meta.service.loadBalancerIP | string | Do not allocate a load balancer IP | Load balancer IP for the meta service |
| meta.service.nodePort | int | Do not allocate a node port | Node port for the meta service |
| meta.service.type | string | `"ClusterIP"` | Service type for the meta service |
| meta.sharedSecret.secret | object | `{"key":"secret","name":"influxdb-enterprise-shared-secret"}` | Shared secret used by the internal API for JWT authentication between InfluxDB nodes. Must have a key named `secret` that should be a long, random string See [documentation for shared-internal-secret](https://docs.influxdata.com/enterprise_influxdb/v1/administration/configure/config-data-nodes/#meta-internal-shared-secret). |
| meta.sharedSecret.secret.key | string | `"secret"` | Key within that secret that contains the shared secret |
| meta.sharedSecret.secret.name | string | `"influxdb-enterprise-shared-secret"` | Name of the secret containing the shared secret |
| meta.tolerations | list | `[]` | Tolerations for meta pods |
| nameOverride | string | `""` | Override the base name for resources |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `false` | Whether to create a Kubernetes service account to run as |
| serviceAccount.name | string | Name based on the chart fullname | Name of the Kubernetes service account to run as |
