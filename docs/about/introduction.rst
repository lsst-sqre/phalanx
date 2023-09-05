#########################################
Overview of the Phalanx platform concepts
#########################################

Rubin Observatory's application deployments, like the Rubin Science Platform, run in Kubernetes_ clusters.
Phalanx is how these application deployments are defined — both generally, and specifically for each Kubernetes cluster.
In a nutshell, Phalanx is a Git repository containing Helm charts for individual applications (like websites and web APIs) that are configured for multiple environments (like different data access centers and production/development versions of each).
`Argo CD`_ instances synchronize these application deployment manifests into the Kubernetes cluster of each environment.

Expanding on that, this page briefly introduces the Phalanx's key features, terminology, and technology ecosystem.

Kubernetes and Docker containers
================================

Phalanx deploys applications on Kubernetes_ clusters — where "cluster" refers to one or more compute nodes that provide CPU, storage, and networking.

Kubernetes_ is a *container orchestration* system.
These Docker_ containers are isolated environments where instances of an application (such as a web API or website) run.
Containers are instances of Docker *images* and those images are the built products of individual application codebases.

Kubernetes layers upon Docker by running multiple containers according to configuration, while also managing the networking and storage needs of those containers.
For application developers, the main interface for defining how an application runs is through resources that are commonly represented as YAML files.

.. sidebar:: Common Kubernetes resources

   A Deployment_ resource defines a set of Pods_ that run simultaneously, and those Pods in turn define one or more containers that run together.
   Deployments and their pods can be configured with ConfigMap_ and Secret_ resources.
   Deployments are made available to the network by defining a Service_.
   An Ingress_ resource publishes that Service to the internet and defines what authentication and authorization is needed.

   You can `learn more about Kubernetes from its documentation <https://kubernetes.io/>`_, and also in Phalanx's :doc:`documentation on creating applications </developers/index>`.

Environments are specific Kubernetes clusters
---------------------------------------------

Phalanx treats specific Kubernetes clusters as separate environments.
Each environment is configured to run specific sets of applications with specific configurations, although all environments running Phalanx benefit from a base of shared applications and Kubernetes-based infrastructure.

Infrastructure agnostic
-----------------------

Although Phalanx *uses* Kubernetes, this platform is agnostic about how Kubernetes itself is deployed for a specific environment.
Phalanx has been deployed on both public clouds (the public Rubin Science Platform runs on the Google Kubernetes Engine) and on-premises Kubernetes clusters (US Data Facility and most international data access centers [IDACs]).
Running on a public cloud versus on-premises generally impacts the specifics of how individual applications are configured.

Helm
====

Helm_ is a tool for packaging applications for deployment in Kubernetes.
Helm *charts* are templates for Kubernetes resources.
By supplying values (i.e., through "values.yaml" files), Helm renders templates for specific Kubernetes environments.

Phalanx takes practical advantage of Helm charts in two ways.
First, each application has a values file for each environment.
This is the key mechanism for how Phalanx supports application deployments across multiple diverse environments.

Second, Helm enables us to deploy existing Helm charts for external open source software.
In some cases, Phalanx application charts are shells around an external Helm chart, such as ingress-nginx.
In other cases, external Helm charts are composed as sub-charts within Phalanx's first-party application — like a Redis cluster within a Rubin API application.

Applications are Helm charts in Phalanx
---------------------------------------

In Phalanx, the word *application* specifically refers to a Helm chart located in the :file:`applications` directory of the `phalanx repository`_.
That Helm chart directory includes the Kubernetes templates and Docker image references to deploy the application, as well as values files to configure the application for each environment.

Argo CD
========

`Argo CD`_ manages the Kubernetes deployments of each application's Helm chart from the Phalanx repository.
Each environment runs its own instance of Argo CD (as Argo CD is itself an application in Phalanx).

Argo CD provides a web UI that shows resources in the Kubernetes cluster, provides lightweight access to logs, and most importantly provides controls for syncing and restarting applications to match the current definitions in the Phalanx GitHub repository.

In development environments, Argo CD's UI makes it possible to temporarily edit Kubernetes resources for testing configurations outside from the Git-based process.
Argo CD replaces most need for the standard Kubernetes command-line client, ``kubectl``.
In fact, most developers for individual applications only have Argo CD access in most environments.

Vault and secrets management
============================

Phalanx adopts Vault_ as its secret store.
Since the `phalanx repository`_ is public, secret cannot be included directly — instead, secrets are referenced from a Vault secret store.
The Vault Secrets Operator connects information in the secret store with Phalanx applications.
Applications that need a secret include a ``VaultSecret`` resource in their Helm chart.
Inside Kubernetes, the `Vault Secrets Operator`_ obtains the secret information from a Vault instance and formats it into a standard Kubernetes Secret_ that the application's containers can consume as environment variables or mounted files.

Phalanx itself does not manage Vault.
Most Rubin Science Platform environments use the Vault server at ``vault.lsst.codes``, which is hosted on `Roundtable`_.
Each installation environment has its own root path in that Vault server.
Phalanx also includes scripts for syncing a 1Password_ vault into the Vault_ service.
See :doc:`secrets` to learn more.

The core applications
=====================

Phalanx includes applications that provide key functionality for other applications:

``argocd`` (application management)
    As described above, Argo CD is an application that synchronizes applications defined in Phalanx with running resources in Kubernetes and provides a UI for developers and administrators.

``cert-manager`` (TLS certificate management)
    Cert-manager acquires and renews TLS certificates from Let's Encrypt.

``gafaelfawr``
    Gafaelfawr is the authentication, access control, and identity management layer of Phalanx.
    Phalanx applications rely on Gafaelfawr to authenticate the user and make most access control decisions, including rate limiting.

``ingress-nginx`` (ingress)
    The ingress-nginx application routes traffic from the internet to individual applications, while also terminating TLS and integrating with Gafaelfawr, the authentication and access control layer.

``vault-secrets-operator`` (secret configuration)
    Vault Secrets Operator bridges secrets in Vault_ with Kubernetes Secret_ resources.

Next steps
==========

This page provided a brief tour of the concepts and components of Phalanx-based application deployments.
For more introductory topics, see the :doc:`index` overview topics.

Start working with Phalanx:

- If you are a developer looking to integrate your application into Phalanx, see the :doc:`/developers/index` section to get started.
- If you are an administrator looking to create a new environment or operate an existing one, see the :doc:`/admin/index` section.
