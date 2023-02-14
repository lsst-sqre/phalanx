###############################
Bootstrapping a new environment
###############################

This is (somewhat incomplete) documentation on how to create a new Rubin Science Platform environment.

Requirements
============

* The installer assumes Git 2.22 or later.

* We presume that you are using Vault_ coupled with `Vault Secrets Operator`_ to manage your Kubernetes secrets, and that all of the secrets for your environment will be stored under a single common prefix.
  See the `LSST Vault Utilities documentation <https://github.com/lsst-sqre/lsstvaultutils#secrets>`__ for the naming convention that we usually use.
  We strongly recommend using the `LSST Vault Utilites`_ to create multiple enclaves (one per instance), so that then compromise of one instance doesn't expose all your secrets for all instances.

* Rubin Science Platform applications expect the public hostname of the Science Platform to have a TLS certificate that can be verified using standard CA roots.
  Using a self-signed certificate or an institutional CA that is not in the normal list of CAs shipped with Docker base images will probably not work.
  See :ref:`hostnames` for more information.

Checklist
=========

.. rst-class:: open

#. Fork the `Phalanx repository`_ if this work is separate from the SQuaRE-managed environments.

#. Create a virtual environment with the tools you will need from the installer's `requirements.txt <https://github.com/lsst-sqre/phalanx/blob/main/installer/requirements.txt>`__.

#. Create a new ``values-<environment>.yaml`` file in `/environments <https://github.com/lsst-sqre/phalanx/tree/main/environments/>`__.
   Start with a template copied from an existing environment that's similar to the new environment.
   Edit it so that ``environment``, ``fqdn``, and ``vaultPathPrefix`` at the top match your new environment.
   Choose which applications to enable or leave disabled.

#. Decide on your approach to TLS certificates.
   See :ref:`hostnames` for more details.
   This may require DNS configuration in Route 53 if this is the first deployment in a new domain and you are using Let's Encrypt for certificates.

#. Do what DNS setup you can.
   If you already know the IP address where your instance will reside, create the DNS records (A or possibly CNAME) for that instance.
   If you are using a cloud provider or something like minikube where the IP address is not yet known, then you will need to create that record once the top-level ingress is created and has an external IP address.

#. Decide on your approach to user home directory storage.
   The Notebook Aspect requires a POSIX file system.
   The most frequently used method of providing that file system is NFS mounts, but you may instead want to use a different file system that's mounted on the Kubernetes cluster nodes and exposed to pods via ``hostPath``.
   Either way, you will need to configure appropriate mount points in :px-app:`nublado2` and :px-app:`moneypenny` when you configure each application in the next step.

#. For each enabled application, create a corresponding ``values-<environment>.yaml`` file in the relevant directory under `/applications <https://github.com/lsst-sqre/phalanx/tree/main/applications/>`__.
   Customization will vary from application to application.
   The following applications have special bootstrapping considerations:

   - :px-app-bootstrap:`argo-cd`
   - :px-app-bootstrap:`cachemachine`
   - :px-app-bootstrap:`gafaelfawr`
   - :px-app-bootstrap:`nublado2`
   - :px-app-bootstrap:`portal`
   - :px-app-bootstrap:`squareone`

#. Generate the secrets for the new environment and store them in Vault with `/installer/update_secrets.sh <https://github.com/lsst-sqre/phalanx/blob/main/installer/update_secrets.sh>`__.
   You will need the write key for the Vault enclave you are using for this environment.
   If you are using 1Password as a source of secrets, you will also need the access token for the 1Password Connect server.
   (For SQuaRE-managed deployments, this is in the ``SQuaRE Integration Access Token: Argo`` 1Password item in the SQuaRE vault.)

#. Run the installer script at `/installer/install.sh <https://github.com/lsst-sqre/phalanx/blob/main/installer/install.sh>`__.
   Debug any problems.
   The most common source of problems are errors or missing configuration in the ``values-<environment>.yaml`` files you created for each application.

#. If the installation is using a dynamically-assigned IP address, while the installer is running, wait until the ingress-nginx-controller Service_ comes up and has an external IP address; then go set the A record for your endpoint to that address (or set an A record with that IP address for the ingress and a CNAME from the endpoint to the A record).
   For installations that are intended to be long-lived, it is worth capturing the IP address at this point and modifying your configuration to use it statically should you ever need to reinstall the instance.

.. _hostnames:

Hostnames and TLS
=================

The Science Platform is designed to run under a single hostname.
``Ingress`` resources for all applications use different routes on the same external hostname.
That hostname, in turn, is served by an NGINX proxy web server, configured via the ``ingress-nginx`` Helm chart.
An NGINX ingress controller is required since its ``auth_request`` mechanism is used for authentication.

The external hostname must have a valid TLS certificate that is trusted by the stock configuration of standard CentOS, Debian, and Alpine containers.
There are supported two mechanisms to configure that TLS certificate:

#. Purchase a commercial certificate and configure it as the ingress-nginx default certificate.
   For more information, see :doc:`/applications/ingress-nginx/certificates`.
   Do not add TLS configuration to any of the application ``Ingress`` resources.
   With this approach, the certificate will have to be manually renewed and replaced at whatever frequency the commercial certificate provider requires.
   Usually this is once per year.

#. Configure Let's Encrypt to obtain a certificate via the DNS solver.
   Once this is configured, TLS will be handled automatically without further human intervention.
   However, this approach is far more complex to set up and has some significant prerequisites.
   For more information, see :px-app-bootstrap:`cert-manager`.

To use the second approach, you must have the following:

* An :abbr:`AWS (Amazon Web Services)` account in which you can create two Route 53 hosted domains.
  You must use this domain for the hostname of the Science Platform installation.
* The ability to delegate to that Route 53 hosted domain from some public DNS domain.
  This means either registering a domain via Amazon, registering a domain elsewhere and pointing it to Amazon's Route 53 DNS servers, or creating a subdomain of an existing public domain by adding ``NS`` records to that domain for a subdomain hosted on Route 53.

If neither of those requirements sound familiar, you almost certainly want to use the first option and purchase a commercial certificate.
