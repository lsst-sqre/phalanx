# onepassword-connect

1Password API server

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| connect.api.resources | object | `{"limits":{"cpu":"1","memory":"32Mi"},"requests":{"cpu":"1m","memory":"15Mi"}}` | Resource requests and limits for connect-api pod |
| connect.connect.credentialsKey | string | `"op-session"` | Name of key inside secret containing 1Password credentials |
| connect.connect.credentialsName | string | `"onepassword-connect-secret"` | Name of secret containing the 1Password credentials |
| connect.connect.serviceType | string | `"ClusterIP"` | Type of service to create |
| connect.sync.resources | object | `{"limits":{"cpu":"1","memory":"32Mi"},"requests":{"cpu":"1m","memory":"10Mi"}}` | Resource requests and limits for connect-sync pod |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
