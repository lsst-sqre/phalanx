# ssp-vet

Web tool for vetting Solar System THOR linkages by eye

## Source Code

* <https://github.com/mjuric/ssp-vet>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the ssp-vet deployment pod |
| data.storageClassName | string | None, must be set | Storage class of the volume holding the input data. At USDF, `sdf-data-rubin` provisions a hostPath of the whole /sdf/data/rubin filesystem, of which the pod mounts only `data.subPath`. |
| data.subPath | string | None, must be set | Path of the input data directory within that volume, mounted read only at `/data` (`SSP_VET_ROOT`). Its files must be readable by the pod's `runAsGroup`. |
| env | object | `{}` | Extra environment variables for the app. The image's defaults already match the mounts this chart makes (`SSP_VET_ROOT=/data`, `SSP_VET_VAR=/var/lib/ssp-vet`). |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the ssp-vet image |
| image.pullSecrets | list | `[]` | Names of image pull secrets in the app's namespace, for a private registry. `ghcr.io/mjuric/ssp-vet` is private, so pulling it requires one. |
| image.repository | string | `"ghcr.io/mjuric/ssp-vet"` | Image to use in the ssp-vet deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.pathPrefix | string | `"/ssp-vet"` | URL path prefix the app is served under. The ingress passes it through and the app strips it itself (`SSP_VET_PATH_PREFIX`). |
| ingress.scope | string | `"exec:portal"` | Gafaelfawr scope required to use the app. The reviewer name the app records comes from the `X-Auth-Request-User` header Gafaelfawr sets. |
| nodeSelector | object | `{}` | Node selection rules for the ssp-vet deployment pod |
| persistence.size | string | `"1Gi"` | Size of the state volume |
| persistence.storageClassName | string | The cluster default | Storage class of the state volume |
| podAnnotations | object | `{}` | Annotations for the ssp-vet deployment pod |
| podSecurityContext | object | `{"runAsGroup":1000,"runAsNonRoot":true,"runAsUser":1000}` | Security context for the pod. `runAsGroup` must be able to read the input data. `fsGroup` is not allowed: the data volume is a hostPath of existing files that must never be chowned. |
| resources | object | See `values.yaml` | Resource limits and requests for the ssp-vet deployment pod |
| tolerations | list | `[]` | Tolerations for the ssp-vet deployment pod |
