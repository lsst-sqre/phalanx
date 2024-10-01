# rapid-analysis

A Helm chart for deploying the Rapid Analysis services.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | This specifies the scheduling constraints of the pod. |
| butlerSecret | object | `{}` | This section allows for specification of Butler secret information. If this section is used, it must contain the following attributes: _key_ (The vault key for the Butler secret), _containerPath_ (The directory location for the Butler secret), _dbUser_ (The username for the Butler backend database) |
| credentialFile | string | `""` | The name of the expected credential file for the broadcasters |
| credentialSecretsPath | string | `""` | The key for the credentials including any sub-paths. |
| env | object | `{}` | This section holds a set of key, value pairs for environmental variables (ENV_VAR: value). NOTE: RUN_ARG is taken care of by the chart using _script_. |
| envSecrets | list | `[]` | This section holds specifications for secret injection. If this section is used, each object listed must have the following attributes defined: _name_ (The label for the secret), _secretName_ (The name of the vault store reference. Uses the _namespace_ attribute to construct the full name), _secretKey_ (The key in the vault store containing the necessary secret) |
| fullnameOverride | string | `""` | Specify the deployed application name specifically. Overrides all other names. |
| gather2aSet | object | `{}` | This configures a StatefulSet used for visit-level gather processing. |
| gatherRollupSet | object | `{}` | This configures a StatefulSet used for night-summary rollup. |
| image.pullPolicy | string | `"IfNotPresent"` | The policy to apply when pulling an image for deployment. |
| image.repository | string | `"ts-dockerhub.lsst.org/rubintv-broadcaster"` | The Docker registry name for the container image. |
| image.tag | string | `"develop"` | The tag of the container image to use. |
| imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. If this section is used, each object listed can have the following attributes defined: _name_ (The label identifying the pull-secret to use) |
| location | string | `""` | Provide the location where the system is running. |
| nameOverride | string | `""` | Adds an extra string to the release name. |
| namespace | string | `"rapid-analysis"` | This is the namespace where the applications will be deployed. |
| nfsMountpoint | list | `[]` | This section holds the information necessary to create a NFS mount for the container. If this section is used, each object listed can have the following attributes defined: _name_ (A label identifier for the mountpoint), _containerPath_ (The path inside the container to mount), _readOnly_ (This sets if the NFS mount is read only or read/write), _server_ (The hostname of the NFS server), _serverPath_ (The path exported by the NFS server) |
| nodeSelector | object | `{}` | This allows the specification of using specific nodes to run the pod. |
| podAnnotations | object | `{}` | This allows the specification of pod annotations. |
| pullSecretsPath | string | `""` |  |
| pvcMountpoint | list | `[]` | This section holds information about existing volume claims. If the section is used, each object listed can have the following attributes defined: _name_ (The name ot the persistent volume), _containerPath_ (The path inside the container to mount), _subPath_ (persistent volume subpath, optional) |
| pvcMountpointClaim | list | `[]` | This section holds the information necessary to claim persistent volumes. If the section is used, each object listed can have the following attributes defined: _name_ (The name ot the persistent volume), _containerPath_ (The path inside the container to mount), _subPath_ (persistent volume subpath, optional) |
| redis.affinity | object | `{}` | Affinity rules for the redis pods |
| redis.enabled | bool | `false` | This specifies whether to use redis or not. |
| redis.env | object | `{}` | This section holds a set of key, value pairs for environmental variables (ENV_VAR: value). NOTE: RUN_ARG is taken care of by the chart using _script_. |
| redis.envSecrets | list | `[]` | This section holds specifications for secret injection. If this section is used, each object listed must have the following attributes defined: _name_ (The label for the secret), _secretName_ (The name of the vault store reference. Uses the _namespace_ attribute to construct the full name), _secretKey_ (The key in the vault store containing the necessary secret) |
| redis.image.pullPolicy | string | `"IfNotPresent"` | The policy to apply when pulling an image for deployment. |
| redis.image.repository | string | `"docker.io/redis"` | The Docker registry name for the redis container image. |
| redis.image.tag | string | `"latest"` | The tag of the redis container image to use. |
| redis.nodeSelector | object | `{}` | Node selection rules for the redis pods |
| redis.resources | object | `{}` | This allows the specification of resources (CPU, memory) requires to run the redis container. |
| redis.storage.classname | string | `nil` |  |
| redis.storage.request | string | `"1Gi"` | The size of the storage request. |
| redis.tolerations | list | `[]` | Toleration specifications for the redis pods |
| resources | object | `{}` | This allows the specification of resources (CPU, memory) requires to run the container. |
| rubinTvSecretsPath | string | `""` |  |
| scripts | object | `{}` | List of script objects to run for the broadcaster. This section MUST have the following attribute specified for each entry. _name_ (The full path for the script) The following attributes are optional _resources_ (A resource object specification) _nodeSelector_ (A node selector object specification) _tolerations_ (A list of tolerations) _affinity_ (An affinity object specification) |
| securityContext | object | `{}` | This section allows for specification of security context information. If the section is used, at least one of the following attributes must be specified. _uid_ (User id to run application as), _gid_ (Group id of the user that runs the application), _fid_ (File system context user id), |
| siteTag | string | `""` | A special tag for letting the scripts know where they are running. |
| tolerations | list | `[]` | This specifies the tolerations of the pod for any system taints. |
| vaultPrefixPath | string | `""` | The Vault prefix path |
| workerSet | object | `{}` | This configures a StatefulSet used for single frame workers. |
