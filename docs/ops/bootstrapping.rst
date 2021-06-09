##############################
Bootstrapping a new deployment
##############################

This is (very incomplete) documentation on how to add a new Rubin Science Platform environment.

Checklist
=========

#. Fork the `phalanx repository <https://github.com/lsst-sqre/phalanx>`__ if this work is separate from the SQuaRE-managed environments.
#. Create a new ``values-<environment>.yaml`` file in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/>`__.
   Start with a template copied from an existing environment that's similar to the new environment.
   Edit it to change the environment name at the top to match ``<environment>`` and choose which services to enable or disable.
#. Decide on your approach to TLS certificates.
   See :ref:`hostnames` for more details.
#. For each enabled service, create a corresponding ``values-<environment>.yaml`` file in the relevant directory under `/services <https://github.com/lsst-sqre/phalanx/tree/master/services/>`__.
   Customization will vary from service to service, but the most common change required is to set the fully-qualified domain name of the environment to the one that will be used for your new deployment.
   This will be needed in ingress hostnames, NGINX authentication annotations, and the paths to Vault secrets (the part after ``k8s_operator`` should be the same fully-qualified domain name).
#. Generate the secrets for the new environment with `/installer/generate_secrets.py <https://github.com/lsst-sqre/phalanx/tree/master/installer/generate_secrets.py>`__ and store them in Vault with `/installer/push_secrets.sh <https://github.com/lsst-sqre/phalanx/tree/master/installer/push_secrets.sh>`__.
#. Run the installer script at `/installer/install.sh <https://github.co/lsst-sqre/phalanx/tree/master/installer/install.sh>`__.

.. _hostnames:

Hostnames and TLS
=================

The Science Platform is designed to run under a single hostname.
All ingresses for all applications use different routes on the same external hostname.
That hostname, in turn, is served by an NGINX proxy web server, configured via the ``ingress-nginx`` Helm chart (normally installed with the Science Platform).
An NGINX ingress controller is required since its ``auth_request`` mechanism is used for authentication.

The external hostname must have a valid TLS certificate that is trusted by the stock configuration of standard CentOS, Debian, and Alpine containers.
There are supported two mechanisms to configure that TLS certificate:

#. Purchase a commercial certificate and configure it as the ingress-nginx default certificate.
   Do not add TLS configuration to any of the application ingresses.
   For more information, see :doc:`ingress-nginx/certificates`.
   With this approach, the certificate will have to be manually renewed and replaced once per year.

#. Configure Let's Encrypt to obtain a certificate via the DNS solver.
   Once this is configured, TLS will be handled automatically without further human intervention.
   However, this approach is far more complex to set up and has some significant prerequisites.
   For more information, see :doc:`cert-issuer/bootstrapping`.

To use the second approach, you must have the following:

* An :abbr:`AWS (Amazon Web Services)` account in which you can create two Route 53 hosted domains.
  You must use this domain for the hostname of the Science Platform installation.
* The ability to delegate to that Route 53 hosted domain from some public DNS domain.
  This means either registering a domain via Amazon, registering a domain elsewhere and pointing it to Amazon's Route 53 DNS servers, or creating a subdomain of an existing public domain by adding ``NS`` records to that domain for a subdomain hosted on Route 53.

If neither of those requirements sound familiar, you almost certainly want to use the first option and purchase a commercial certificate.

Application notes
=================

Gafaelfawr
----------

When creating the Gafaelfawr configuration for a new environment, in addition to choosing between OpenID Connect authentication and GitHub authentication, you will need to define a group mapping.
This specifies which scopes a user will receive based on which groups they are a member of in the upstream identity system.
The current default expects the NCSA groups, which will not be accurate unless you're using CILogon with NCSA LDAP as an attribute source.

The most important scopes to configure are:

* ``exec:admin``: provides access to administrative tools (users do not need this)
* ``exec:user``: allows users to create personal tokens
* ``exec:notebook``: allows users to use the Notebook Aspect
* ``exec:portal``: allows users to use the Portal Aspect
* ``read:tap``: allows users to make TAP queries

If you are using OpenID Connect, the group values for each scope should be group names as shown in the ``isMemberOf`` claim.

If you are using GitHub, group membership will be synthesized from all of the teams of which the user is a member.
These must be team memberships, not just organization memberships.
The corresponding group for Gafaelfawr purposes will be ``<organization>-<team>`` where ``<team>`` is the team **slug**, not the team name.
That means the team name will be converted to lowercase and spaces will be replaced with dashes, and other transformations will be done for special characters.
For more information about how Gafaelfawr constructs groups from GitHub teams, see `the Gafaelfawr documentation <https://gafaelfawr.lsst.io/arch/providers.html#github-groups>`__.

For an example of a ``group_mapping`` configuration for GitHub authentication, see `/services/gafaelfawr/values-idfdev.yaml <https://github.com/lsst-sqre/phalanx/tree/master/services/gafaelfawr/values-idfdev.yaml>`__.

If you run into authentication problems, see :doc:`the Gafaelfawr operational documentation <gafaelfawr/index>` for debugging instructions.

Squareone
---------

If you are using the Let's Encrypt approach to obtain TLS certificates, you must give the Squareone ingress with an appropriate TLS configuration.

Because all application ingresses share the same external hostname, the way the ingress configuration is structured is somewhat unusual.
Nearly all of the services create an ingress without adding TLS configuration.
Instead, they all use the same hostname, without a TLS stanza.
The Squareone ingress is the one designated ingress with a TLS configuration to request creation of certificates.
Because each ingress uses the same hostname, the NGINX ingress will merge all of those ingresses into one virtual host and will set up TLS if TLS is defined on any of them.

Were TLS defined on more than one ingress, only one of those TLS configurations would be used, but which one is chosen is somewhat random.
Therefore, we designate a single application to hold the configuration to avoid any confusion from unused configurations.

This means adding something like the following to ``values-<environment>.yaml`` in `/services/squareone <https://github.com/lsst-sqre/phalanx/tree/master/services/squareone>`__:

.. code-block:: yaml

   squareone:
     ingress:
       host: "rsp.example.com"
       annotations:
         cert-manager.io/cluster-issuer: cert-issuer-letsencrypt-dns
       tls:
         - secretName: squareone-tls
           hosts:
             - "rsp.example.com"
