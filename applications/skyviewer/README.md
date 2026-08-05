# skyviewer

Sky imagery browser for private HiPS surveys

## Source Code

* <https://github.com/lsst-dm/skyviewer-client>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the skyviewer deployment pod |
| config.apiUrl | string | `"https://api.skyviewer.app/api"` | Craft CMS GraphQL API, used for page content and tours. Imagery comes from `hipsSurvey`, not from here. |
| config.astroApiUrl | string | `"https://us-central1-edc-prod-eef0.cloudfunctions.net/astro-objects-api"` | Astro objects API, used by the search panel. |
| config.cloudEnv | string | `"PROD"` | PROD, INT or DEV. DEV additionally enables the GCS proxy route and the debug UI. |
| config.hipsDataDir | string | `"/sdf/group/rubin/shared/hips_views"` | Directory holding the HiPS surveys. Must sit below `hipsData.mountPath`. |
| config.hipsSurvey | string | `""` | Path below `hipsDataDir` of the single survey to display, e.g. `LSSTCam/hips/ltl2/color_gri`. The CMS advertises public datasets absent from this tree, so without this the viewer offers surveys whose every tile 404s. |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| hipsData | object | See `values.yaml` | Volumes holding the HiPS surveys, mounted read-only. More than one is usually needed: /sdf/group/rubin/shared is a symlink to /sdf/data/rubin/shared, so mounting only the group export leaves the surveys unreachable through a dangling symlink. |
| hipsData.enabled | bool | `true` | Whether to mount the HiPS volumes. Without them the viewer has no imagery. |
| hipsData.mounts | list | `[{"capacity":"1Gi","mountPath":"/sdf/group/rubin","name":"sdf-group-rubin","storageClassName":"sdf-group-rubin"},{"capacity":"1Gi","mountPath":"/sdf/data/rubin","name":"sdf-data-rubin","storageClassName":"sdf-data-rubin"}]` | Claims to create and mount. Each entry needs `name`, `storageClassName`, `capacity` and `mountPath`. `config.hipsDataDir` must resolve below one of them, following symlinks. |
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
