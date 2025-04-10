# atlantis

Tool for github terraform workflows: https://runatlantis.io

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the atlantis deployment pod |
| config.automerge | bool | `false` | Whether to automatically merge PRs after plans have been applied (see [docs](https://www.runatlantis.io/docs/automerging.html)) |
| config.logLevel | string | `"info"` | Log level for the Atlantis server. Must be one of: debug, info, warn, or error. |
| config.repoAllowList | list | `[]` | The GitHub repos that atlantis will accept webooks from: [docs](https://www.runatlantis.io/docs/server-configuration.html#repo-allowlist) |
| config.serverConfig | object | `{"repos":[{"apply_requirements":["approved","mergeable","undiverged"],"id":"/.*/","import_requirements":["approved","mergeable"]}]}` | Content for the [server-side repo config](https://www.runatlantis.io/docs/server-side-repo-config.html) file |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the atlantis image |
| image.repository | string | `"ghcr.io/lsst-sqre/atlantis-custom"` | atlantis image to use |
| image.tag | string | The appVersion of the chart | Tag of atlantis image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the atlantis ingresses |
| nodeSelector | object | `{}` | Node selection rules for the atlantis deployment pod |
| podAnnotations | object | `{}` | Annotations for the atlantis deployment pod |
| resources | object | See `values.yaml` | Resource limits and requests for the atlantis deployment pod |
| tolerations | list | `[]` | Tolerations for the atlantis deployment pod |
