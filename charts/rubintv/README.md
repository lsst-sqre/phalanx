# rubintv

Real-time display front end

## Source Code

* <https://github.com/lsst-ts/rubintv>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| frontend.affinity | object | `{}` | Affinity rules for the rubintv frontend pod |
| frontend.debug | bool | `false` | If set to true, enable more verbose logging. |
| frontend.image | object | `{"pullPolicy":"IfNotPresent","repository":"ghcr.io/lsst-ts/rubintv","tag":""}` | Settings for rubintv OCI image |
| frontend.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the rubintv image |
| frontend.image.repository | string | `"ghcr.io/lsst-ts/rubintv"` | rubintv frontend image to use |
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
| imagePullSecrets | list | See `values.yaml` | Image pull secrets. |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nameOverride | string | `""` | Override the base name for resources |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"rubintv-secrets"` | Name of secret containing Redis password (may require changing if fullnameOverride is set) |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage and thus tokens. Setting this to false will use `emptyDir` and reset all tokens on every restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"1Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| separateSecrets | bool | `true` | Whether to use the new secrets management scheme |
| siteTag | string | `""` | A special tag for letting the scripts know where they are running.  Must be overridden at each site |
| workers.affinity | object | `{}` | Affinity rules for the rubintv worker pods |
| workers.debug | bool | `false` | If set to true, enable more verbose logging. |
| workers.env | list | `[]` | This section holds a list of key, value pairs for environmental variables (name: key, value: value). |
| workers.envSecrets | list | See `values.yaml` | This section holds specifications for secret injection. |
| workers.gid | string | `nil` | GID to run as (site-dependent as above) |
| workers.image | object | `{"pullPolicy":"IfNotPresent","repository":"ts-dockerhub.lsst.org/rubintv-broadcaster","tag":"develop"}` | Settings for OCI image for worker pods |
| workers.image.pullPolicy | string | `"IfNotPresent"` | The policy to apply when pulling an image for deployment. |
| workers.image.repository | string | `"ts-dockerhub.lsst.org/rubintv-broadcaster"` | The Docker registry name for the container image. |
| workers.image.tag | string | `"develop"` | The tag of the container image to use. |
| workers.imagePullSecrets | list | See `values.yaml` | Image pull secrets. |
| workers.nfsMountpoint | list | See `values.yaml` | NFS mountpoints for the rubintv worker pods |
| workers.nodeSelector | object | `{}` | Node selector rules for the rubintv worker pods |
| workers.pathPrefix | string | `"/"` | Prefix for the (internal) worker API routes |
| workers.podAnnotations | object | `{}` | Annotations for the rubintv worker pods |
| workers.pvcMountpoint | list | See `values.yaml` | PVC claims for the rubintv worker pods |
| workers.replicas | int | `0` | how many replicas to use |
| workers.resources | object | `{}` | Resource limits and requests for the rubintv worker pods |
| workers.script | string | `"slac/rubintv/workerPod1.py"` | Script that runs in RUN_ARG.  This dynamic mechanism needs to be replaced with something less scary, but there is resistance to that, at least while iterating. |
| workers.scriptsLocation | string | `"/repos/rubintv_production/scripts"` | The location of the scripts folder where the worker pod will run specific scripts, set by RUN_ARG. |
| workers.tolerations | list | `[]` | Tolerations for the rubintv worker pods |
| workers.uid | string | `nil` | UID to run as (site-dependent because of filesystem access; must be specified) |
