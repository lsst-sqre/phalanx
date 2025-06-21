# eups-distributor

Distributes EUPS binaries

## Source Code

* <https://github.com/lsst-dm/distrib-docker>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the eups-distributor deployment pod |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the eups-distributor image |
| image.repository | string | `"ghcr.io/lsst-dm/distrib-docker"` | Image to use in the eups-distributor deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress."nginx.ingress.kubernetes.io/preserve-trailing-slash" | string | `"true"` |  |
| ingress.hostname | string | `""` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the eups-distributor deployment pod |
| podAnnotations | object | `{"gke-gcsfuse/cpu-limit":"10","gke-gcsfuse/cpu-request":"500m","gke-gcsfuse/ephemeral-storage-request":"50Gi","gke-gcsfuse/memory-limit":"10Gi","gke-gcsfuse/memory-request":"1Gi","gke-gcsfuse/volumes":"true"}` | Annotations for the eups-distributor deployment pod |
| pvc.name | string | `"gke-ssd"` |  |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the eups-distributor deployment pod |
| tolerations | list | `[]` | Tolerations for the eups-distributor deployment pod |
| volumes.claimName | string | `"gke-ssd"` |  |
| volumes.name | string | `"gke-gcsfuse-cache"` |  |
