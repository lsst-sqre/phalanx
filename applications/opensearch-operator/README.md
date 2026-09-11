# opensearch-operator

OpenSearch Kubernetes Operator

## Source Code

* <https://github.com/opensearch-project/opensearch-k8s-operator>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| manager.extraEnv | list | `[]` |  |
| manager.loglevel | string | `"info"` |  |
| manager.watchNamespace | string | `nil` |  |
