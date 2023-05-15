# csc

A Helm chart for deploying the Control System CSCs.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | This specifies the scheduling constraints of the pod |
| annotations | object | `{}` | This allows the specification of pod annotations |
| butlerSecret | object | `{}` | This key allows for specification of Butler secret information. **NOTE**: You must fill out a _secretPermFixer_ entry in addition. If this section is used, it must contain the following attributes: _containerPath_ (The directory location for the Butler secret), _dbUser_ (The username for the Butler backend database) |
| configfile | object | `{}` | This key allows specification of a YAML configuration file If this section is used, it must contain the following attributes defined: _path_ (The container path for the configuration file), _filename_ (The configuration file name), _content_ (The YAML content for the configuration file) |
| enabled | bool | `false` | Flag to enable the given CSC application |
| entrypoint | string | `nil` | This key allows specification of a script to override the entrypoint |
| env | object | `{}` | This is the namespace in which the CSC will be placed |
| envSecrets | list | `[]` | This section holds specifications for secret injection. If this section is used, each object listed must have the following attributes defined: _name_ (The label for the secret), _secretName_ (The name of the vault store reference. Uses the _namespace_ attribute to construct the full name), _secretKey_ (The key in the vault store containing the necessary secret) |
| image.pullPolicy | string | `"IfNotPresent"` | The policy to apply when pulling an image for deployment |
| image.repository | string | `"lsstts/test"` | The Docker registry name of the container image to use for the CSC |
| image.tag | string | `nil` | The tag of the container image to use for the CSC |
| imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. If this section is used, each object listed can have the following attributes defined: _name_ (The label identifying the pull-secret to use) |
| isPrimary | bool | `true` | This marks the CSC as the primary object to sync upon system starts. This is set to false when two CSCs of the same flavor are deployed (one real, one simulator) to mark the simulator so it can be filtered out for automatic syncing. |
| nameOverride | string | `""` | Provide an alternate name for the application |
| nfsMountpoint | list | `[]` | This section holds the information necessary to create a NFS mount for the container. If this section is used, each object listed can have the following attributes defined: _name_ (A label identifier for the mountpoint), _path_ (The path inside the container to mount), _readOnly_ (This sets if the NFS mount is read only or read/write), _server_ (The hostname of the NFS server), _serverPath_ (The path exported by the NFS server) |
| nodeSelector | object | `{}` | This allows the specification of using specific nodes to run the pod |
| pvcMountpoint | list | `[]` | This section holds the information necessary to create a volume mount for the container. If this section is used, each object listed can have the following attributes defined: _name_ (A label identifier for the mountpoint), _path_ (The path inside the container to mount), _accessMode_ (This sets the required access mode for the volume mount), _claimSize_ (The requested physical disk space size for the volume mount), _storageClass_ (The Kubernetes provided storage class), _ids.uid_ (OPTIONAL: An alternative UID for mounting), _ids.gid_ (OPTIONAL: An alternative GID for mounting) |
| resources | object | `{}` | This allows the specification of resources (CPU, memory) requires to run the container |
| secretPermFixer | object | `{}` | This section sets the optional use of an init container for fixing permissions on secret files. If this section is used, each object listed can have the necessary attributes specified: _name_ (The label used for the init container) _containerPath_ (The path in the container where the secret files will be stored) _secretName_ (OPTIONAL: The secret name if different from _name_) _specialInstructions_ (OPTIONAL: This allows for optional instructions to be used when fixing permissions) |
| securityContext | object | `{}` | This key allows for the specification of a pod security context for volumes. If this section is used, it must contain the following attributes: _user_ (The user id for the volumes) _group_ (The group id for the volumes) _fsGroup_ (OPTIONAL: A special supplemental group that applies to all containers in a pod) |
| service.port | int | `nil` | The port number to use for the Service. |
| service.type | string | `nil` | The Service type for the application. This is either ClusterIP (internal access) or LoadBalancer (external access) |
| service.use | bool | `false` | This sets the use of a Service API for the application |
| tolerations | list | `[]` | This specifies the tolerations of the pod for any system taints |
