# rubintv

Continuous integration testing

## Source Code

* <https://github.com/lsst-sqre/rubin-tv>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| frontend.config.debug | bool | `false` | If set to true, enable more verbose logging. |
| frontend.config.pathPrefix | string | `"/rubintv"` | Prefix for rubintv's frontend API routes. |
| frontend.image.affinity | object | `{}` | Affinity rules for the rubintv frontend pod |
| frontend.image.nodeSelector | object | `{}` | Node selector rules for the rubintv frontend pod |
| frontend.image.podAnnotations | object | `{}` | Annotations for the rubintv frontend pod |
| frontend.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the rubintv image |
| frontend.image.repository | string | `"ghcr.io/lsst-sqre/rubintv"` | rubintv frontend image to use |
| frontend.image.resources | object | `{}` | Resource limits and requests for the rubintv frontend pod |
| frontend.image.tag | string | The appVersion of the chart | Tag of rubintv image to use |
| frontend.image.tolerations | list | `[]` | Tolerations for the rubintv frontend pod |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nameOverride | string | `""` | Override the base name for resources |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"rubintv-secret"` | Name of secret containing Redis password (may require changing if fullnameOverride is set) |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"1Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| workers.config.affinity | object | `{}` | Affinity rules for the rubintv worker pods |
| workers.config.butlerSecret | object | `{}` | This section allows for specification of Butler secret information. If this section is used, it must contain the following attributes: _key_ (The vault key for the Butler secret), _containerPath_ (The directory location for the Butler secret), _dbUser_ (The username for the Butler backend database) |
| workers.config.credentialFile | string | `""` | The name of the expected credential file for the broadcasters |
| workers.config.credentialSecretsPath | string | `""` | The key for the credentials including any sub-paths. |
| workers.config.debug | bool | `false` | If set to true, enable more verbose logging. |
| workers.config.env | object | `{}` | This section holds a set of key, value pairs for environmental variables (ENV_VAR: value). NOTE: RUN_ARG is taken care of by the chart using _script_. |
| workers.config.envSecrets | list | `[]` | This section holds specifications for secret injection. If this section is used, each object listed must have the following attributes defined: _name_ (The label for the secret), _secretName_ (The name of the vault store reference. Uses the _namespace_ attribute to construct the full name), _secretKey_ (The key in the vault store containing the necessary secret) |
| workers.config.gid | int | `1000` | GID to run as |
| workers.config.image.pullPolicy | string | `"IfNotPresent"` | The policy to apply when pulling an image for deployment. |
| workers.config.image.repository | string | `"ts-dockerhub.lsst.org/rubintv-broadcaster"` | The Docker registry name for the container image. |
| workers.config.image.tag | string | `"develop"` | The tag of the container image to use. |
| workers.config.imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. If this section is used, each object listed can have the following attributes defined: _name_ (The label identifying the pull-secret to use) |
| workers.config.nfsMountpoint | list | `[]` | This section holds the information necessary to create a NFS mount for the container. If this section is used, each object listed can have the following attributes defined: _name_ (A label identifier for the mountpoint), _containerPath_ (The path inside the container to mount), _readOnly_ (This sets if the NFS mount is read only or read/write), _server_ (The hostname of the NFS server), _serverPath_ (The path exported by the NFS server) |
| workers.config.nodeSelector | object | `{}` | Node selector rules for the rubintv worker pods |
| workers.config.pathPrefix | string | `"/"` | Prefix for the (internal) worker API routes |
| workers.config.podAnnotations | object | `{}` | Annotations for the rubintv worker pods |
| workers.config.pullSecretsPath | string | `""` |  |
| workers.config.pvcMountpoint | list | `[]` | This section holds information about existing volume claims. If the section is used, each object listed can have the following attributes defined: _name_ (The name ot the persistent volume), _containerPath_ (The path inside the container to mount), _subPath_ (persistent volume subpath, optional) |
| workers.config.pvcMountpointClaim | list | `[]` | This section holds the information necessary to claim persistent volumes. If the section is used, each object listed can have the following attributes defined: _name_ (The name ot the persistent volume), _containerPath_ (The path inside the container to mount), _subPath_ (persistent volume subpath, optional) |
| workers.config.resources | object | `{}` | Generic resource limits and requests for the rubintv worker pods |
| workers.config.scripts | obj | `[]` | List of script objects to run for the broadcaster. This section MUST have the following attribute specified for each entry. _name_ (The full path for the script) The following attributes are optional _resources_ (A resource object specification) _nodeSelector_ (A node selector object specification) _tolerations_ (A list of tolerations) _affinity_ (An affinity object specification) |
| workers.config.tolerations | list | `[]` | Tolerations for the rubintv worker pods |
| workers.config.uid | int | `1000` | UID to run as (site-dependent, because of filesystem perms) |
| workers.config.vaultPrefixPath | string | `""` | The Vault prefix path |
| workers.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the rubintv worker image |
| workers.image.repository | string | `"docker.io/lsstts/rubintv-broadcaster"` | rubintv worker image to use |
| workers.image.tag | string | None, must be set per-deployment | Tag of rubintv worker image to use |
