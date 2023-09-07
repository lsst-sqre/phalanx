# cert-manager

TLS certificate manager

**Homepage:** <https://cert-manager.io/>

## Source Code

* <https://github.com/cert-manager/cert-manager>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cert-manager.cainjector.extraArgs | list | `["--logging-format=json"]` | Additional arguments to the CA injector |
| cert-manager.extraArgs | list | `["--logging-format=json","--dns01-recursive-nameservers-only","--dns01-recursive-nameservers=8.8.8.8:53,1.1.1.1:53"]` | Additional arguments to the main cert-manager pod |
| cert-manager.installCRDs | bool | `true` | Whether to install CRDs |
| cert-manager.webhook.extraArgs | list | `["--logging-format=json"]` | Additional arguments to the webhook pod |
| config.createIssuer | bool | `true` | Whether to create a Let's Encrypt DNS-based cluster issuer |
| config.email | string | sqre-admin | Contact email address registered with Let's Encrypt |
| config.route53.awsAccessKeyId | string | None, must be set if `createIssuer` is true | AWS access key ID for Route 53 (must match `aws-secret-access-key` in Vault secret referenced by `config.vaultSecretPath`) |
| config.route53.hostedZone | string | None, must be set if `createIssuer` is true | Route 53 hosted zone in which to create challenge records |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
