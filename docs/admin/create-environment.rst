################################
Create a new Phalanx environment
################################

Each separate installation of Phalanx is called an environment.
An environment has a hostname, Vault server and path to its secrets, and a set of Phalanx applications that should be installed in that environment.

Each Phalanx environment must be installed in a separate Kubernetes cluster.
Two Phalanx environments cannot coexist in the same cluster.

Before starting this process, ensure that you have met the :doc:`requirements to run Phalanx <requirements>` and that you have decided on your :doc:`handling of hostnames and TLS <hostnames>`.

Creating an environment
=======================

To create a new Phalanx environment, take the following steps:

.. rst-class:: open

#. Fork the `Phalanx repository`_ if this work is separate from the SQuaRE-managed environments.

#. Create a new :file:`values-{environment}.yaml` file in `environments <https://github.com/lsst-sqre/phalanx/tree/main/environments/>`__.
   Start with a template copied from an existing environment that's similar to the new environment.
   Edit it so that ``name``, ``fqdn``, ``vaultUrl``, and ``vaultPathPrefix`` at the top match your new environment.
   You may omit ``vaultUrl`` for SQuaRE-managed environments.
   See :doc:`secrets-setup` for more information about the latter two settings and additional settings you may need.
   If the environment will be hosted on Google Kubernetes Engine, also fill out ``gcp.projectId``, ``gcp.region``, and ``gcp.clusterName`` with metadata about where the environment will be hosted.
   Enable the applications this environment should include.

#. Do what DNS setup you can.
   If you already know the IP address where your instance will reside, create the DNS records (A or possibly CNAME) for that instance.
   If you are using a cloud provider or something like minikube where the IP address is not yet known, then you will need to create that record once the top-level ingress is created and has an external IP address.

#. Decide on your approach to user home directory storage.
   The Notebook Aspect (the ``nublado`` application) requires a POSIX file system.
   The most frequently used method of providing that file system is NFS mounts, but you may instead want to use persistent volume claims or a different file system that's mounted on the Kubernetes cluster nodes and exposed to pods via ``hostPath``.
   Whatever storage you choose, you will need to configure appropriate mount points in :px-app:`nublado` when you configure each application in the next step.

#. For each enabled application, create a corresponding :file:`values-{environment}.yaml` file in the relevant directory under `applications <https://github.com/lsst-sqre/phalanx/tree/main/applications/>`__.
   Customization will vary from application to application.
   The following applications have special bootstrapping considerations:

   - :px-app-bootstrap:`argocd`
   - :px-app-bootstrap:`gafaelfawr`
   - :px-app-bootstrap:`nublado`
   - :px-app-bootstrap:`portal`

#. Add the URL of your new environment to :file:`docs/documenteer.toml` under ``phinx.linkcheck.ignore``.
   The Argo CD URL of your environment will be unreachable, so you need to tell Sphinx valid link checking to ignore it.

Next steps
==========

- Define the secrets for your new environment and store them in Vault: :doc:`secrets-setup`
