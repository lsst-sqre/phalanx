# csc_collector

A Helm chart provided shared information for Control System CSCs.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| namespace | string | `""` | Namespace for shared CSC resources. |
| secrets | list | `[]` | This section holds secret specifications. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the secret) _key_ (The key in the vault store where the secret resides) _type_ (OPTIONAL: The secret type. Defaults to Opaque.) |
| siteTag | string | `""` | The site-specific name used for handling configurable CSCs |
