# onepassword-connect

1Password API server

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| connect.connect.credentialsKey | string | `"op-session"` | Name of key inside secret containing 1Password credentials |
| connect.connect.credentialsName | string | `"onepassword-connect-secret"` | Name of secret containing the 1Password credentials |
| connect.connect.serviceType | string | `"ClusterIP"` | Type of service to create |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
