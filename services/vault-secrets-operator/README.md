# vault-secrets-operator

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://ricoberger.github.io/helm-charts/ | vault-secrets-operator | 1.18.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| vault-secrets-operator.environmentVars[0] | object | `{"name":"VAULT_TOKEN","valueFrom":{"secretKeyRef":{"key":"VAULT_TOKEN","name":"vault-secrets-operator"}}}` | environment variable where the Vault read token is kept |
| vault-secrets-operator.environmentVars[1] | object | `{"name":"VAULT_TOKEN_LEASE_DURATION","valueFrom":{"secretKeyRef":{"key":"VAULT_TOKEN_LEASE_DURATION","name":"vault-secrets-operator"}}}` | environment variable storing the lease duration, in seconds |
| vault-secrets-operator.vault.address | string | `"https://vault.lsst.codes"` | URL of the underlying Vault implementation |
| vault-secrets-operator.vault.reconciliationTime | int | `60` | Sync secrets from vault on this cadence |
