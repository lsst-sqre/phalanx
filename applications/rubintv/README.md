# rubintv

Continuous integration testing

## Source Code

* <https://github.com/lsst-sqre/rubin-tv>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| frontend.affinity | object | `{}` | Affinity rules for the rubintv frontend pod |
| frontend.debug | bool | `false` | If set to true, enable more verbose logging. |
| frontend.image | object | `{"pullPolicy":"IfNotPresent","repository":"ghcr.io/lsst-sqre/rubintv","tag":""}` | Settings for rubintv OCI image |
| frontend.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the rubintv image |
| frontend.image.repository | string | `"ghcr.io/lsst-sqre/rubintv"` | rubintv frontend image to use |
| frontend.image.tag | string | The appVersion of the chart | Tag of rubintv image to use |
| frontend.nodeSelector | object | `{}` | Node selector rules for the rubintv frontend pod |
| frontend.pathPrefix | string | `"/rubintv"` | Prefix for rubintv's frontend API routes. |
| frontend.podAnnotations | object | `{}` | Annotations for the rubintv frontend pod |
| frontend.resources | object | `{}` | Resource limits and requests for the rubintv frontend pod |
| frontend.tolerations | list | `[]` | Tolerations for the rubintv frontend pod |
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
| siteTag | string | `""` | A special tag for letting the scripts know where they are running.  Must be overridden at each site |
| workers.affinity | object | `{}` | Affinity rules for the rubintv worker pods |
| workers.butlerSecret | object | `{}` | This section allows for specification of Butler secret information. If this section is used, it must contain the following attributes: _key_ (The vault key for the Butler secret), _containerPath_ (The directory location for the Butler secret), _dbUser_ (The username for the Butler backend database) |
| workers.credentialFile | string | `""` | The name of the expected credential file for the broadcasters |
| workers.credentialSecretsPath | string | `""` | The key for the credentials including any sub-paths. |
| workers.debug | bool | `false` | If set to true, enable more verbose logging. |
| workers.env | list | `[]` | This section holds a list of key, value pairs for environmental variables (name: key, value: value). NOTE: RUN_ARG is taken care of by the chart using _script_. |
| workers.envSecrets | list | `[]` | This section holds specifications for secret injection. If this section is used, each object listed must have the following attributes defined: _name_ (The label for the secret), _secretName_ (The name of the vault store reference. Uses the _namespace_ attribute to construct the full name), _secretKey_ (The key in the vault store containing the necessary secret) |
| workers.gid | int | `1000` | GID to run as |
| workers.image | object | `{"pullPolicy":"IfNotPresent","repository":"ts-dockerhub.lsst.org/rubintv-broadcaster","tag":"develop"}` | Settings for OCI image for worker pods |
| workers.image.pullPolicy | string | `"IfNotPresent"` | The policy to apply when pulling an image for deployment. |
| workers.image.repository | string | `"ts-dockerhub.lsst.org/rubintv-broadcaster"` | The Docker registry name for the container image. |
| workers.image.tag | string | `"develop"` | The tag of the container image to use. |
| workers.imagePullSecrets | list | `[]` |  |
| workers.nodeSelector | object | `{}` | Node selector rules for the rubintv worker pods |
| workers.pathPrefix | string | `"/"` | Prefix for the (internal) worker API routes |
| workers.podAnnotations | object | `{}` | Annotations for the rubintv worker pods |
| workers.pullSecretsPath | string | `""` |  |
| workers.replicas | int | `5` | how many replicas to use |
| workers.resources | object | `{}` | Resource limits and requests for the rubintv worker pods |
| workers.script | string | `"slac/rubintv/workerPod1.py"` | Script that runs in RUN_ARG.  This needs to be replaced with something less scary |
| workers.tolerations | list | `[]` | Tolerations for the rubintv worker pods |
| workers.uid | int | `1000` | UID to run as (site-dependent, because of filesystem perms) |
| workers.vaultPrefixPath | string | `""` | The Vault prefix path |
| workers.volumes | list | `[]` | Volumes for the rubintv worker pods If this section is used, each list item must contain the following attributes: _name_ (the name of the volume) _accessMode_ (ReadOnly, ReadWriteOnce, ReadWriteMany) _mountPath_ (path mounted into the container) and at least one of _persistentVolumeClaim_ or _nfs_ _persistentVolumeClaim_ has fields _name_ (the name of the PVC) _storageClass_ (the storage class of the PVC) _capacity_ (the size (as a string) of the PVC (e.g. "1Gi")) _nfs_ is not yet implemented |
