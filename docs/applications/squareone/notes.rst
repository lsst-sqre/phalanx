.. px-app-notes:: squareone

################################
Squareone architecture and notes
################################

TLS configuration merging
=========================

This applies only to environments that use Let's Encrypt for certificate management.

Because all application ingresses share the same external hostname, the way the ingress configuration is structured in Phalanx is somewhat unusual.
Nearly all application create an ingress without adding TLS configuration.
Instead, they all use the same hostname, without a TLS stanza.
The Squareone ingress is the one designated ingress with a TLS configuration to request creation of certificates.
Because each ingress uses the same hostname, the NGINX ingress will merge all of those ingresses into one virtual host and will set up TLS if TLS is defined on any of them.

Were TLS defined on more than one ingress, only one of those TLS configurations would be used, but which one is chosen is somewhat random.
Therefore, we designate Squareone as the single application to hold the configuration to avoid any confusion from unused configurations.
