# gke

Resources specific to GKE clusters

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| autopilot.singleZones | list | `[]` | An autopilot compute class that only provisions nodes in a single zone will be provisioned for every zone in this list. |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
