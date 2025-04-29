# atlantis

Tool for github terraform workflows: https://runatlantis.io

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the atlantis deployment pod |
| config.repoAllowList | list | `[]` | The GitHub repos that atlantis will accept webooks from: [docs](https://www.runatlantis.io/docs/server-configuration.html#repo-allowlist) |
| config.repoConfig | object | See `values.yaml` | Content for the [server-side repo config](https://www.runatlantis.io/docs/server-side-repo-config.html) file |
| config.serverConfig | object | See `values.yaml` | Content for the [server config](https://www.runatlantis.io/docs/server-configuration.html) file. Note the format of the keys (kebab-case) |
| config.serverConfig.automerge | bool | `false` | Whether to automatically merge PRs after plans have been applied (see [docs](https://www.runatlantis.io/docs/automerging.html)) |
| config.serverConfig.log-level | string | `"info"` | One of: debug, info, warn, or error. |
| config.serverConfig.repo-allowlist | list | `[]` | The GitHub repos that atlantis will accept webooks from: [docs](https://www.runatlantis.io/docs/server-configuration.html#repo-allowlist) |
| config.serverConfig.web-basic-auth | bool | `false` | We're delegating auth for the web UI to gafaelfawr |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the atlantis image |
| image.repository | string | `"ghcr.io/lsst-sqre/atlantis-custom"` | atlantis image to use |
| image.tag | string | The appVersion of the chart | Tag of atlantis image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the atlantis ingresses |
| nodeSelector | object | `{}` | Node selection rules for the atlantis deployment pod |
| persistence | object | See `values.yaml` | Persistent storage configuration. Atlantis stores Terraform plans and git repo clones while pull requests are open. This data is deleted when the pull requests are merged or closed. |
| persistence.size | string | `"5Gi"` | Amount of persistent storage to request |
| persistence.storageClass | string | `nil` | Class of storage to request |
| podAnnotations | object | `{}` | Annotations for the atlantis deployment pod |
| resources | object | See `values.yaml` | Resource limits and requests for the atlantis deployment pod |
| tolerations | list | `[]` | Tolerations for the atlantis deployment pod |
