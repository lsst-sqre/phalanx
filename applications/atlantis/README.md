# atlantis

Tool for github terraform workflows: https://runatlantis.io

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the atlantis deployment pod |
| githubRepoAllowList | list | `[]` | The GitHub repos that atlantis will accept webooks from: [docs](https://www.runatlantis.io/docs/server-configuration.html#repo-allowlist) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the atlantis image |
| image.repository | string | `"ghcr.io/runatlantis/atlantis"` | atlantis image to use |
| image.tag | string | The appVersion of the chart | Tag of atlantis image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the atlantis deployment pod |
| podAnnotations | object | `{}` | Annotations for the atlantis deployment pod |
| resources | object | See `values.yaml` | Resource limits and requests for the atlantis deployment pod |
| tolerations | list | `[]` | Tolerations for the atlantis deployment pod |
