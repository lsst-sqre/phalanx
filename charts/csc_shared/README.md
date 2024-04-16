# csc_shared

A Helm chart provided shared information for Control System CSCs.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| pullSecrets | list | `[]` | This section holds pull secret specifications. NOTE: The pull secret is expected to be part of the pull-secret key in Vault. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the pull secret) |
