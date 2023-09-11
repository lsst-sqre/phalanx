# onepassword-connect-dev

1Password API server (dev)

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| idfdev.connect.applicationName | string | `"connect-idfdev"` | Name of the Kubernetes Deployment |
| idfdev.connect.credentialsKey | string | `"op-session"` | Name of key inside secret containing 1Password credentials |
| idfdev.connect.credentialsName | string | `"idfdev-secret"` | Name of secret containing the 1Password credentials |
| idfdev.connect.serviceType | string | `"ClusterIP"` | Type of service to create |
