# skyviewer

Sky imagery browser for private HiPS surveys

## Source Code

* <https://github.com/lsst-dm/skyviewer-client>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the skyviewer deployment pod |
| config.apiUrl | string | `""` | Craft CMS GraphQL API, used for page content and tours. Required. Imagery comes from `hipsSurvey`, not from here. |
| config.astroApiUrl | string | `""` | Astro objects API, used by the search panel. Required. |
| config.cloudEnv | string | `"PROD"` | PROD, INT or DEV. DEV additionally enables the GCS proxy route and the debug UI. |
| config.hipsDataDir | string | `""` | Directory holding the HiPS surveys. Must resolve below one of `hipsData.mounts`, following symlinks. Required when `hipsData.enabled` is true. |
| config.hipsSurvey | string | `""` | Path below `hipsDataDir` of the single survey to display, e.g. `LSSTCam/hips/ltl2/color_gri`. The CMS advertises public datasets absent from this tree, so without this the viewer offers surveys whose every tile 404s. |
| config.tileCacheBytes | string | `"0"` | Byte cap for the in-memory FIFO cache of served tiles; "0" disables it. The pod serves all tile traffic itself, so without it every tile is re-read from networked disk on every request. Must fit inside the memory limit with room for the application itself. |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| hipsData | object | See `values.yaml` | Volumes holding the HiPS surveys, mounted read-only. All of this is specific to where the surveys are staged, so it is set per environment. |
| hipsData.enabled | bool | `false` | Whether to mount the HiPS volumes. Without them the viewer has no imagery, so an environment that enables it must also set `config.hipsDataDir`, `mounts` and usually `supplementalGroups`. |
| hipsData.mounts | list | `[]` | Claims to create and mount. Each entry needs `name`, `storageClassName`, `capacity` and `mountPath`. `config.hipsDataDir` must resolve below one of them, following symlinks. |
| hipsData.supplementalGroups | list | `[]` | Supplemental group IDs the pod runs with. The exports holding the surveys are typically group-readable only, and without the right group every read is denied even with the volumes mounted. |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the skyviewer image |
| image.repository | string | `"ghcr.io/lsst-dm/skyviewer-client"` | Image to use in the skyviewer deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| imagePullSecrets | list | See `values.yaml` | Image pull secrets. Needed only while the GHCR package is private; a public package pulls without credentials. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| ingress.path | string | `"/skyviewer"` | Path the app is served under. Must match the NEXT_PUBLIC_BASE_PATH the image was built with: Next.js compiles its base path into the client bundle, so the two cannot be changed independently. |
| nodeSelector | object | `{}` | Node selection rules for the skyviewer deployment pod |
| podAnnotations | object | `{}` | Annotations for the skyviewer deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the skyviewer deployment pod |
| tolerations | list | `[]` | Tolerations for the skyviewer deployment pod |
