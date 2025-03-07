# plot-navigator

Plot-navigator

## Source Code

* <https://github.com/lsst-dm/plot-navigator>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.persistentVolumeClaims | list | `[]` | PersistentVolumeClaims to create. |
| config.separateSecrets | bool | `true` | Whether to use the new secrets management scheme |
| config.volume_mounts | list | `[]` | Mount points for additional volumes |
| config.volumes | list | `[]` | Additional volumes to attach |
| environment | object | `{}` | Environment variables (e.g. butler configuration/auth parms) for the nextjs server |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.repository | string | `"ghcr.io/lsst-dm/plot-navigator"` | plot-navigator image to use |
| image.tag | string | The appVersion of the chart | Tag of plot-navigator image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| redis.config.secretKey | string | `"password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"redis-secret"` | Name of secret containing Redis password |
| resources | object | see `values.yaml` | Resource limits and requests for the nodejs pod |
