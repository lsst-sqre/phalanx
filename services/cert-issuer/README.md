# cert-issuer

Set up a cert-manager cluster issuer for a Science Platform environment.
Only used in environments where we control our own certificates.
The issuer is separate from the cert-manager application because on the base and summit clusters cert-manager is managed by IT but without the issuer that we want to use.

This chart also creates a certificate for the `fqdn` value configured in the environment-specific `values-*.yaml`.
The resulting secret is in `default-certificate` and can be referenced in the configuration of the `ingress-nginx` chart.
This is done for backwards compatibility and eventually will be replaced by ingress-specific configuration everywhere.
