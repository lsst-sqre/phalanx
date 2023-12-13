################################
Installing a Phalanx environment
################################

Each separate installation of Phalanx is called an environment.
An environment has a hostname, Vault server and path to its secrets, and a set of Phalanx applications that should be installed in that environment.

Before starting this process, you should set up the required secrets for your new environment.
See :doc:`secrets-setup` for details.

If you are setting up an environment that will be running a 1Password Connect server for itself, you will need to take special bootstrapping steps.
See :px-app-bootstrap:`onepassword-connect` for more information.

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

#. Decide on your approach to TLS certificates.
   See :doc:`hostnames` for more details.
   This may require DNS configuration in Route 53 if this is the first deployment in a new domain and you are using Let's Encrypt for certificates.

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
   - :px-app-bootstrap:`cachemachine`
   - :px-app-bootstrap:`gafaelfawr`
   - :px-app-bootstrap:`portal`
   - :px-app-bootstrap:`squareone`

#. Add the URL of your new environment to :file:`docs/documenteer.toml` under ``phinx.linkcheck.ignore``.
   The Argo CD URL of your environment will be unreachable, so you need to tell Sphinx valid link checking to ignore it.

Installing Phalanx
==================

Once you have defined a Phalanx environment, follow these steps to install it.
These can be run repeatedly to reinstall Phalanx over an existing deployment.

#. Create a Vault AppRole that will be used by Vault Secrets Operator.

   .. prompt:: bash

      phalanx vault create-read-approle <environment>

   Be aware that this will invalidate any existing AppRole for that environment.

#. Run the installer script at `installer/install.sh <https://github.com/lsst-sqre/phalanx/blob/main/installer/install.sh>`__.

   .. prompt:: bash

      installer/install.sh <enviornment> <vault-role-id> <vault-secret-id>

   ``<vault-role-id>`` and ``<vault-secret-id>`` are the Role ID and Secret ID of the Vault AppRole created in the previous step.

   Debug any problems.
   The most common source of problems are errors or missing configuration in the :file:`values-{environment}.yaml` files you created for each application.
   You can safely run the installer repeatedly as you debug and fix issues.

#. If the installation is using a dynamically-assigned IP address, while the installer is running, wait until the ingress-nginx-controller service comes up and has an external IP address.
   Then, set the A record for your endpoint to that address (or set an A record with that IP address for the ingress and a CNAME from the endpoint to the A record).
   For installations that are intended to be long-lived, it is worth capturing this IP address at this point and modifying the ``ingress-nginx`` configuration to use it statically should you ever need to reinstall the instance.
