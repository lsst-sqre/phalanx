# uws

Deployment for the UWS and DM OCPS CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.controlSystemAppNamespace | string | Set by ArgoCD | Application namespacce for the control system deployment |
| global.controlSystemImageTag | string | Set by ArgoCD | Image tag for the control system deployment |
| global.controlSystemKafkaBrokerAddress | string | Set by ArgoCD | Kafka broker address for the control system deployment |
| global.controlSystemKafkaTopicReplicationFactor | string | Set by ArgoCD | Kafka topic replication factor for control system topics |
| global.controlSystemS3EndpointUrl | string | Set by ArgoCD | S3 endpoint (LFA) for the control system deployment |
| global.controlSystemSchemaRegistryUrl | string | Set by ArgoCD | Schema registry URL for the control system deployment |
| global.controlSystemSiteTag | string | Set by ArgoCD | Site tag for the control system deployment |
| global.controlSystemTopicName | string | Set by ArgoCD | Topic name tag for the control system deployment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| atocps.enabled | bool | `false` | Enable the OCPS:1 CSC |
| ccocps.enabled | bool | `false` | Enable the OCPS:2 CSC |
| csc_collector.secrets | list | `[]` | This section holds secret specifications. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the secret) _key_ (The key in the vault store where the secret resides) _type_ (OPTIONAL: The secret type. Defaults to Opaque.) |
| mtocps.enabled | bool | `false` | Enable the OCPS:3 CSC |
| uws-api-server.basePath | string | `"uws-server"` | The base path for the client ingress |
| uws-api-server.butlerPg | object | `{}` | Configuration for Postgres backed butlers The object must have the following attributes defined: _secretKey_ (A label that points to the VaultSecret for the postgres credentials) _containerPath_ (The directory location in the container for the Butler secret) _dbUser_ (The database user name for butler access) |
| uws-api-server.client.enabled | bool | `false` | Turn on the UWS client system if desired |
| uws-api-server.createNamespace | bool | `false` | Temporary flag to make service deploy own namespace. Doing this to not disrupt other sites. |
| uws-api-server.hostname | string | `""` | Hostname for the client ingress |
| uws-api-server.image.repository | string | `"lsstdm/uws-api-server"` | The Docker registry name of the UWS server container image |
| uws-api-server.image.tag | string | `"latest"` | The tag of the UWS server container image |
| uws-api-server.job.image.repository | string | `"lsstsqre/centos"` | The Docker registry name of the UWS job container image |
| uws-api-server.job.image.tag | string | `"d_latest"` | The tag of the UWS job container image |
| uws-api-server.job.securityContext.fsGroup | int | `202` | Set the filesystem GID for the mounted volumes in the UWS job container |
| uws-api-server.job.securityContext.runAsGroup | int | `202` | Set the GID for the UWS job container entrypoint |
| uws-api-server.job.securityContext.runAsUser | int | `1000` | Set the UID for the UWS job container entrypoint |
| uws-api-server.logLevel | string | `"WARNING"` | Log level of server. Set to "DEBUG" for highest verbosity |
| uws-api-server.replicaCount | int | `1` | Set the replica count for the UWS server |
| uws-api-server.server.securityContext.fsGroup | int | `202` | Set the filesystem GID for the mounted volumes in the UWS server container |
| uws-api-server.server.securityContext.runAsGroup | int | `202` | Set the GID for the UWS server container entrypoint |
| uws-api-server.server.securityContext.runAsUser | int | `1000` | Set the UID for the UWS server container entrypoint |
| uws-api-server.targetCluster | string | `""` | Target Kubernetes cluster |
| uws-api-server.vaultPathPrefix | string | `""` | Site-specific Vault path for secrets. |
| uws-api-server.volumes | list | `[]` | Central data volumes to be mounted in job containers. Each object listed can have the following attributes defined: _name_ (A label identifier for the data volume mount) _server_ (The hostname for the NFS server with the data volume mount) _claimName_ (The PVC claim name for the data volume mount) _mountPath_ (The mount path in the server container for the data volume mount) _exportPath_ (The export path on the NFS server for the data volume mount) _subPath_ (A possible sub path for the data volume mount) _readOnly_ (Flag to mark the data volume mount as read only or read/write) |
| uws-api-server.workingVolume.claimName | string | `""` | The PVC claim name for the working volume |
| uws-api-server.workingVolume.exportPath | string | `""` | The export path on the NFS server for the working volume |
| uws-api-server.workingVolume.mountPath | string | `"/uws"` | The mount path in the server container for the working volume |
| uws-api-server.workingVolume.name | string | `"job-files"` | A label identifier for the working volume |
| uws-api-server.workingVolume.server | string | `""` | The hostname for the NFS server with the working volume |
| uws-api-server.workingVolume.subPath | string | `""` | A possible sub path for the working volume mount |
