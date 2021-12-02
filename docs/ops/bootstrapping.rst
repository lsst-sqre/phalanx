##############################
Bootstrapping a new deployment
##############################

This is (somewhat incomplete) documentation on how to add a new Rubin Science Platform environment.

Requirements
============

* The installer assumes Git 2.22 or later.

* We presume that you are using `Vault <https://www.vaultproject.io/>`__ coupled with `Vault Secrets Operator <https://github.com/ricoberger/vault-secrets-operator>`__ to manage your Kubernetes secrets, and further that you will use the same taxonomy that SQuaRE does as described in the `LSST Vault Utilities <https://github.com/lsst-sqre/lsstvaultutils#secrets>`__ documentation (essentially ``secret/k8s_operator/<instance-name>``).
  We strongly recommend using the `LSST Vault Utilites <https://github.com/lsst-sqre/lsstvaultutils/>`__ to create multiple enclaves (one per instance), so that then compromise of one instance doesn't expose all your secrets for all instances.

* Rubin Science Platform applications expect the public hostname of the Science Platform to have a TLS certificate that can be verified using standard CA roots.
  Using a self-signed certificate or an institutional CA that is not in the normal list of CAs shipped with Docker base images will probably not work.
  See :ref:`hostnames` for more information.

Checklist
=========

#. Fork the `phalanx repository <https://github.com/lsst-sqre/phalanx>`__ if this work is separate from the SQuaRE-managed environments.

#. Create a virtual environment with the tools you will need from the installer's `requirements.txt <https://github.com/lsst-sqre/phalanx/tree/master/installer/requirements.txt>`__.
   If you are not using 1password as your source of truth (which, if you are not in a SQuaRE-managed environment, you probably are not) then you may omit ``1password``.
   In any event, note the write key for your Vault enclave.

#. Create a new ``values-<environment>.yaml`` file in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/>`__.
   Start with a template copied from an existing environment that's similar to the new environment.
   Edit it to change the environment name at the top to match ``<environment>`` and choose which services to enable or disable.

#. Decide on your approach to TLS certificates.
   See :ref:`hostnames` for more details.

#. Do what DNS setup you can.
   If you already know the IP address where your instance will reside, create the DNS records (A or possibly CNAME) for that instance.
   If you are using a cloud provider or something like minikube where the IP address is not yet known, then you will need to create that record once the top-level ingress is created and has an external IP address.

   The first time you set up the RSP for a given domain (note: *not* hostname, but *domain*, so if you were setting up ``dev.my-rsp.net`` and ``prod.my-rsp.net``, ``dev`` first, you would only need to do this when you created ``dev``), if you are using Let's Encrypt for certificate management (which we highly recommend), you will need to create glue records to enable Let's Encrypt to manage TLS for the domain.
   See :doc:`cert-issuer/route53-setup` for more details.

#. For each enabled service, create a corresponding ``values-<environment>.yaml`` file in the relevant directory under `/services <https://github.com/lsst-sqre/phalanx/tree/master/services/>`__.
   Customization will vary from service to service, but the most common change required is to set the fully-qualified domain name of the environment to the one that will be used for your new deployment.
   This will be needed in ingress hostnames, NGINX authentication annotations, and the paths to Vault secrets (the part after ``k8s_operator`` should be the same fully-qualified domain name).

   See :ref:`service-notes` for more details on special considerations for individual services.

#. Generate the secrets for the new environment with `/installer/generate_secrets.py <https://github.com/lsst-sqre/phalanx/tree/master/installer/generate_secrets.py>`__ and store them in Vault with `/installer/push_secrets.sh <https://github.com/lsst-sqre/phalanx/tree/master/installer/push_secrets.sh>`__.
   This is where you will need the write key for the Vault enclave.

#. Run the installer script at `/installer/install.sh <https://github.co/lsst-sqre/phalanx/tree/master/installer/install.sh>`__.

   If the installation is using a dynamically-assigned IP address, while the installer is running, wait until the ingress-nginx-controller service comes up and has an external IP address; then go set the A record for your endpoint to that address (or set an A record with that IP address for the ingress and a CNAME from the endpoint to the A record).
   For installations that are intended to be long-lived, it is worth capturing the IP address at this point and modifying your configuration to use it statically should you ever need to reinstall the instance.

.. _hostnames:

Hostnames and TLS
=================

The Science Platform is designed to run under a single hostname.
All ingresses for all services use different routes on the same external hostname.
That hostname, in turn, is served by an NGINX proxy web server, configured via the ``ingress-nginx`` Helm chart (normally installed with the Science Platform).
An NGINX ingress controller is required since its ``auth_request`` mechanism is used for authentication.

The external hostname must have a valid TLS certificate that is trusted by the stock configuration of standard CentOS, Debian, and Alpine containers.
There are supported two mechanisms to configure that TLS certificate:

#. Purchase a commercial certificate and configure it as the ingress-nginx default certificate.
   Do not add TLS configuration to any of the service ingresses.
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

.. _service-notes:

Service notes
=============

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

Nublado 2
---------

Nublado (the ``nublado2`` service) and moneypenny need to know where the NFS server that provides user home space is.
Nublado also requires other persistent storage space.
Ensure the correct definitions are in place in their configuration.

For T&S deployments that require instrument control, make sure you have any Multus network definitions you need in the ``nublado2`` ``values.yaml``.
This will look something like:

.. code-block:: yaml

    singleuser:
      extraAnnotations:
        k8s.v1.cni.cncf.io/networks: "kube-system/auxtel-dds, kube-system/comcam-dds, kube-system/misc-dds"
      initContainers:
        - name: "multus-init"
          image: "lsstit/ddsnet4u:latest"
          securityContext:
            privileged: true

The Multus network names are given as an annotation string containing the networks, separated by commas.
Experimentally, it appears that the interfaces will appear in the order specified.

The ``initContainers`` entry should be inserted verbatim.
It creates a privileged container that bridges user pods to the specified networks before releasing control to the user's lab.

Portal
------

If the Portal Aspect is configured with a ``replicaCount`` greater than one (recommended for production installations), ``firefly_shared_workdir`` must be set and point to an underlying filesystem that supports shared multiple-write.
This is **not** supported by most Kubernetes persistent volume backends.

At GKE, we use Filestore via NFS.
At NCSA, we use a ``hostPath`` mount of an underlying GPFS volume.

Currently the provisioning of this underlying backing store is manual, so make sure you either have created it or gotten a system administrator with appropriate permissions for your site to do so.

The default UID for the Portal Aspect is 91, although it is tunable in the deployment if need be.

Squareone
---------

If you are using the Let's Encrypt approach to obtain TLS certificates, you must give the Squareone ingress with an appropriate TLS configuration.

Because all service ingresses share the same external hostname, the way the ingress configuration is structured is somewhat unusual.
Nearly all of the services create an ingress without adding TLS configuration.
Instead, they all use the same hostname, without a TLS stanza.
The Squareone ingress is the one designated ingress with a TLS configuration to request creation of certificates.
Because each ingress uses the same hostname, the NGINX ingress will merge all of those ingresses into one virtual host and will set up TLS if TLS is defined on any of them.

Were TLS defined on more than one ingress, only one of those TLS configurations would be used, but which one is chosen is somewhat random.
Therefore, we designate a single service to hold the configuration to avoid any confusion from unused configurations.

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
