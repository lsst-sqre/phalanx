# flink

Apache Flink Kubernetes Operator

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| flink.enabled | bool | `true` | Whether to enable the Flink Kubernetes Operator |
| flink.operatorPod | object | `{"resources":{"limits":{"cpu":"4","memory":"2Gi"},"requests":{"cpu":"1","memory":"512Mi"}}}` | Kubernetes requests and limits for the Flink Job Manager |
| flink.watchNamespaces | list | `["sasquatch"]` | List of kubernetes namespaces to watch for FlinkDeployment changes |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
