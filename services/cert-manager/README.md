# cert-manager

Set up cert-manager for a Science Platform environment.
Only used in environments where we control our own certificates.
This Helm chart, in addition to installing the upstream cert-manager Helm chart, creates a Let's Encrypt issuer and a certificate for the `fqdn` value configured in the environment-specific `values-*.yaml`.
The resulting secret is `default-certificate` and can be referenced in the configuration of the `nginx-ingress` chart.
