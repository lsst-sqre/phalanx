# cert-manager

Let's Encrypt certificate management

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://charts.jetstack.io | cert-manager | v1.8.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cert-manager | object | Install CRDs, force use of Google and Cloudfront DNS servers | Configuration for upstream cert-manager chart |
| config.createIssuer | bool | `true` | Whether to create a Let's Encrypt DNS-based cluster issuer |
| config.email | string | sqre-admin | Contact email address registered with Let's Encrypt |
| config.route53.awsAccessKeyId | string | None, must be set if `createIssuer` is true | AWS access key ID for Route 53 (must match `aws-secret-access-key` in Vault secret referenced by `config.vaultSecretPath`) |
| config.route53.hostedZone | string | None, must be set if `createIssuer` is true | Route 53 hosted zone in which to create challenge records |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| nameOverride | string | `""` | Override the base name for resources |
