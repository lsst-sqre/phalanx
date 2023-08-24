####################
Phalanx requirements
####################

In order to install a Phalanx environment, the following prerequisites must be in place.

Deployment environment
======================

Phalanx can only be installed in environments that meet the following reuqirements:

- Phalanx is a Kubernetes deployment platform that installs within a Kubernetes cluster.
  The oldest version of Kubernetes known to work is 1.23.
  Phalanx is regularly tested on the stable and rapid channels of Google Kubernetes Engine and will normally support any Kubernetes version up to the current GKE rapid channel default.

- An external authentication system for users must be provided.
  Phalanx supports using GitHub authentication, OpenID Connect, or (as a special case of OpenID Connect) CILogon_.
  GitHub authentication is the easiest way to get started, but requires authorization be managed using GitHub teams, which becomes awkward with scale.

- Metadata about users (full name, email address, group membership, and, if the ``nublado`` application is deployed, UID and GIDs) must be provided by some external system.
  Phalanx supports claims in a JWT from OpenID Connect, GitHub user metadata, or LDAP.
  For LDAP, Phalanx supports simple binds or GSS-API binds using Kerberos.
  Phalanx can also manage UIDs and GIDs itself using Google Firestore as long as the other user metadata is provided by an external source and the UIDs and GIDs can be internal to the Phalanx deployment.

- Phalanx must manage its own ingresses using the included ``ingress-nginx`` application.
  It relies heavily on the specific features and configuration of NGINX that are configured by that Phalanx application.
  It will not work with an external ingress controller that is not managed by Phalanx.

- All secrets management is done using Vault_.
  An external Vault server that is compatible with `Vault Secrets Operator`_ must be available to store Phalanx secrets.

- An external managed PostgreSQL-compatible database server is not strictly required but is strongly recommended.
  Phalanx can deploy an in-cluster PostgreSQL server for test and development environments, but that server is not backed up and is not intended for production use.

Using a Kubernetes networking layer that enforces ``NetworkPolicy`` objects is not required, but is strongly recommended.
Without such an enforcement layer, all users and applications in the Phalanx cluster are trusted and will be able to impersonate arbitrary users to other services.

You will also need to manage TLS certificates for the public hostname or hostnames of your Phalanx environment, although Phalanx may be able to automate this for you.
See :doc:`hostnames` for more information.

Management tooling
==================

Installing Phalanx requires the following tools be available:

- Python 3.11 or later.
  Phalanx expects users of its tooling to use a venv_ and install Python packages from PIP, so its prerequisite Python modules need not be installed locally.
  See :doc:`/about/local-environment-setup` for details on how to set up a local environment suitable for running Phalanx tooling.

- Helm v3 or later.
  (See the `Helm installation instructions <https://helm.sh/docs/intro/install/>`__.)

- Argo CD's command-line tool.
  It may be necessary to update this regularly to match the version of Argo CD that Phalanx, since Argo CD tends to break backward compatibility for its command-line API.
  To see the version of the client that is currently tested, search for ``argocd-linux`` in `.github/workflows/ci.yaml <https://github.com/lsst-sqre/phalanx/blob/main/.github/workflows/ci.yaml>`__.

- The Vault command-line client.
  Any recent version of the client should work.
  To see the version currently used for testing, search for ``vault_`` in `.github/workflows/ci.yaml <https://github.com/lsst-sqre/phalanx/blob/main/.github/workflows/ci.yaml>`__.

- Git 2.22 or later.
