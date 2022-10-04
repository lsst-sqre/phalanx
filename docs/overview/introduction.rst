#########################################
Overview of the Phalanx platform concepts
#########################################

Rubin Observatory's service deployments, like the Rubin Science Platform, run in Kubernetes_ clusters.
Phalanx is how these service deployments are defined — both generally, and specifically for each Kubernetes cluster.
In a nutshell, Phalanx is a Git repository containing Helm charts for individual services (like websites and web APIs) that are configured for multiple environments (like different data access centers and production/development versions of each).
Argo CD instances synchronize these service definitions into the Kubernetes cluster of each environment.

Expanding on that, this page briefly introduces the Phalanx's key features, terminology, and technology ecosystem.

Kubernetes and Docker containers
================================

Phalanx deploys services on Kubernetes_ clusters — where "cluster" refers to one or more compute nodes that provide CPU, storage, and networking.

Kubernetes_ is a *container orchestration* system.
These Docker_ containers are isolated environments where instances of an application (such as a web API or website) run.
Containers are instances of Docker *images* and those images are the built products of individual application codebases.

Kubernetes layers upon Docker by running multiple containers according to configuration, while also managing the networking and storage needs of those containers.
For service developers, the main interface for defining how a service runs is through resources that are represented commonly as YAML files.

.. sidebar:: Common Kubernetes resources

   A Deployment_ resource defines a set of Pods_ that run simultaneously, and those Pods in turn define one or more containers that run together.
   Deployments and their pods can be configured with ConfigMap_ and Secret_ resources.
   Deployments are made available to the network by defining a Service_.
   An Ingress_ resource publishes that Service to the internet and defines what authentication and authorization is needed.

   You can `learn more about Kubernetes from its documentation <https://kubernetes.io/>`_, and also in Phalanx's :doc:`documentation on creating services </service-guide/index>`.

Environments are specific Kubernetes clusters
---------------------------------------------

Phalanx treats specific Kubernetes clusters as environments.
Each environment is configured to run specific sets of services with specific services, although all environments running Phalanx benefit from a base of shared services and Kubernetes-based infrastructure.

Infrastructure agnostic
-----------------------

Although Phalanx *uses* Kubernetes, this platform is agnostic about how Kubernetes itself is deployed for a specific environment.
Phalanx has been deployed on both public clouds (the public Rubin Science Platform runs on the Google Kubernetes Engine) and on-premises Kubernetes clusters (US Data Facility and most international data access centers (IDACs).
Running on a public cloud versus on-premises generally impacts the specifics of how individual services are configured.

Helm
====

Helm_ is a tool for packaging services for deployment in Kubernetes.
Helm charts are templates for Kubernetes resources.
By supplying values (i.e., through "values.yaml" files), these templates are rendered for specific Kubernetes environments.

Phalanx takes practical advantage of Helm charts in two ways.
First, each service has a values file for the each environment.
This is the key mechanism for how Phalanx supports service deployments for multiple diverse environments.

Second, Helm enables us to deploy existing Helm charts for external open source software.
In some cases, Phalanx services are shells around an external Helm chart such as ingress-nginx.
In other cases, external Helm charts are composed as sub-charts within Phalanx's first-party services — like a Redis service within a Rubin API service.

Services are Helm charts in Phalanx
-----------------------------------

In Phalanx, the word "service" specifically refers to a Helm chart located in the :file:`services` directory of the `phalanx repository`_.
That Helm chart directory includes the Kubernetes templates and Docker image references to deploy the application, as well as values files to configure the service for each environment.

Argo CD
=======

Argo CD manages the Kubernetes deployments of each service's Helm charts from the Phalanx repository.
Each environment runs its own instance of Argo CD (as Argo CD is itself a service in Phalanx).

Argo CD provides a web UI that shows resources in the Kubernetes cluster, provides lightweight access to logs, and most importantly provides controls for syncing and restarting services to match the current definitions in the Phalanx GitHub repository.

In development environments, Argo CD's UI makes possible to edit Kubernetes resources to temporarily test configurations separate from the Git-based process.
Argo CD replaces most need for the standard Kubernetes command line client, kubectl.
In fact, most maintainers for individual services only have Argo CD access in most environments.

Vault and secrets management
============================

Phalanx adopts Vault_ as its secret store.
Since the `phalanx repository`_ is public, secret cannot be included directly — instead, secrets are referenced from a Vault secret store.
The Vault Secrets Operator connects information in the secret store with Phalanx services.
Services that need a secret include a ``VaultSecret`` resource.
Inside Kubernetes, the `Vault Secrets Operator`_ obtains the secret information from a Vault instance and formats it into a standard Kubernetes Secret_ that the service's containers can consume as environment variables or mounted files.

Phalanx itself does not manage Vault.
Most Rubin Science Platform installations use the Vault server at ``vault.lsst.codes``, which is managed using `Roundtable`_.
Each installation environment has its own root path in that Vault server.
Phalanx also includes scripts for syncing a 1Password_ vault into the Vault_ service.
See :doc:`secrets` to learn more.

The core services
=================

Phalanx includes services that provide key functionality for other services:

``argocd`` (service management)
    As described above, Argo CD is a service that synchronizes services defined in Phalanx with running resources in Kubernetes and provides a UI for operators.

``cert-manager`` (TLS certificate management)
    Cert-manager acquires and renews TLS certificates from Let's Encrypt.

``ingress-nginx`` (ingress)
    The ingress-nginx service routes traffic from the internet to individual services, while also terminating TLS and integrating with Gafaelfawr, the auth handler.

``vault-secrets-operator`` (secret configuration)
    Vault Secrets Operator bridges secrets in Vault_ with Kubernetes secrets resources.

Next steps
==========

This page provided a brief tour of the concepts and components of Phalanx-based service deployments.
For more introductory topics, see the :doc:`index` overview topics.

Start working with Phalanx:

- If you are a service developer looking to integrate your service into Phalanx, see the :doc:`Service maintainer's guide </service-guide/index>` to get started.
- If you are an operator looking to create a new environment or operate an existing one, see the :doc:`Operator's guide </ops/index>`
