# nvr-control

NVR camera illuminator control

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the nvr-control deployment pod |
| config.configVolume.storageClass | string | `nil` | Storage class for configuration persistent volume |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the nvr-control image |
| image.repository | string | `"ghcr.io/home-assistant/home-assistant"` | Image to use in the nvr-control deployment |
| image.tag | string | `"2025.4"` | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the nvr-control deployment pod |
| podAnnotations | object | `{}` | Annotations for the nvr-control deployment pod |
| resources | object | See `values.yaml` | Resource limits and requests for the nvr-control deployment pod |
| tolerations | list | `[]` | Tolerations for the nvr-control deployment pod |
