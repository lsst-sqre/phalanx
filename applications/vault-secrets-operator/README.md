# vault-secrets-operator

## Source Code

* <https://github.com/ricoberger/vault-secrets-operator>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| vault-secrets-operator.environmentVars | list | Use a Vault AppRole (see `values.yaml` for details) | Additional environment variables used to configure the operator |
| vault-secrets-operator.serviceAccount.createSecret | bool | `false` | Disable creation of a secret for the service account. It shouldn't be needed and it conflicts with the secret we create that contains the credentials for talking to Vault. |
| vault-secrets-operator.vault.address | string | Set by Argo CD | URL of the underlying Vault implementation |
| vault-secrets-operator.vault.authMethod | string | `"approle"` | Authentication method to use |
| vault-secrets-operator.vault.reconciliationTime | int | `60` | Sync secrets from vault on this cadence |
