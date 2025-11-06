# eups-distributor

Distributes EUPS binaries

## Source Code

* <https://github.com/lsst-dm/distrib-docker>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the eups-distributor deployment pod |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the eups-distributor image |
| image.repository | string | `"ghcr.io/lsst-dm/distrib-docker"` | Image to use in the eups-distributor deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress."nginx.ingress.kubernetes.io/preserve-trailing-slash" | string | `"true"` |  |
| ingress.hostname | string | `""` | Additional annotations for the ingress rule |
| lsstDotCodes.awsAccessKeyId | string | `"AKIAQSJOS2SFBNRYNM4I"` |  |
| lsstDotCodes.email | string | `"sqre-admin@lists.lsst.org"` | Contact email address registered with Let's Encrypt |
| lsstDotCodes.enabled | bool | `false` |  |
| lsstDotCodes.hostedZoneId | string | `"Z06873202D7WVTZUFOQ42"` |  |
| lsstDotCodes.hostname | string | `nil` |  |
| nodeSelector | object | `{}` | Node selection rules for the eups-distributor deployment pod |
| podAnnotations | object | `{"gke-gcsfuse/volumes":"true"}` | Annotations for the eups-distributor deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the eups-distributor deployment pod |
| tolerations | list | `[]` | Tolerations for the eups-distributor deployment pod |
