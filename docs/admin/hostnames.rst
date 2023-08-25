#################
Hostnames and TLS
#################

Phalanx environments must have one primary hostname.
Some applications can be deployed under other hostnames, but only resources deployed under the primary hostname can be protected by its standard authentication system.

This external hostname must have a valid TLS certificate that is trusted by the stock configuration of standard CentOS, Debian, and Alpine containers.

There are supported two mechanisms to configure that TLS certificate:

#. Configure Let's Encrypt to obtain a certificate via the DNS solver.
   Once this is configured, TLS will be handled automatically without further human intervention.
   This is the recommended approach.
   For more information, see :px-app-bootstrap:`cert-manager`.

#. Purchase a commercial certificate and configure it as the ingress-nginx default certificate.
   For more information, see :doc:`/applications/ingress-nginx/certificates`.
   Do not add TLS configuration to any of the application ``Ingress`` resources.
   With this approach, the certificate will have to be manually renewed and replaced at whatever frequency the commercial certificate provider requires.
   Usually this is at least once per year.

To use the first approach, you must have the following:

* An :abbr:`AWS (Amazon Web Services)` account in which you can create two Route 53 hosted domains.
  You must use this domain for the hostname of the Science Platform installation.
* The ability to delegate to that Route 53 hosted domain from some public DNS domain.
  This means either registering a domain via Amazon, registering a domain elsewhere and pointing it to Amazon's Route 53 DNS servers, or creating a subdomain of an existing public domain by adding ``NS`` records to that domain for a subdomain hosted on Route 53.

If neither of those requirements sound familiar, you almost certainly want to use the second option and purchase a commercial certificate.
