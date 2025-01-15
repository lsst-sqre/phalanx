################################
Installing a Phalanx environment
################################

Once you have :doc:`created the configuration for your new environment <create-environment>` and :doc:`set up secrets <secrets-setup>`, you are ready to do the installation.

If you are setting up an environment that will be running a 1Password Connect server for itself, you will need to take special bootstrapping steps.
See :px-app-bootstrap:`onepassword-connect` for more information.

.. warning::

   Before starting this process, ensure that you have met the :doc:`requirements to run Phalanx <requirements>`.

   If you get a message indicating that Argo CD login has failed, this usually indicates that you have too old of a version of the ``argocd`` command-line tool installed.
   Update it ``argocd`` and try again.
   See :ref:`admin-tooling` for more details.

Installing Phalanx
==================

Follow these steps to install Phalanx.
These can be run repeatedly to reinstall Phalanx over an existing deployment.

#. Create a Vault AppRole that will be used by Vault Secrets Operator.
   This will invalidate any existing AppRole for that environment.

   Set the ``VAULT_TOKEN`` environment variable to a token with the ability to create new AppRoles (for SQuaRE clusters, use the admin token), and then run:

   .. prompt:: bash

      phalanx vault create-read-approle <environment>

   Unset ``VAULT_TOKEN`` when this command finishes.

#. Set the environment variables ``VAULT_ROLE_ID`` and ``VAULT_SECRET_ID`` to the Role ID and Secret ID printed out by that command.
   Do not otherwise store these values.
   If you need to start over, return to the previous step and generate new values.

#. If you are doing a complete reinstallation of a Phalanx instance, such as when the Kubernetes cluster has been completely destroyed and recreated, you may want to regenerate all generated secrets.
   This ensures that any left-over or leaked secrets that do not come from your static secrets store are invalidated.

   To do this, run :command:`phalanx secrets sync --regenerate <environment>`.
   This will invalidate all existing Gafaelfawr tokens and will require redoing portions of the Sasquatch setup.

#. Ensure that your default Kubernetes cluster for :command:`kubectl` and :command:`helm` is set to point to the Kubernetes cluster into which you want to install the Phalanx environment.
   You can verify this with :command:`kubectl config current-context`.

#. Start the install:

   .. prompt:: bash

      phalanx environment install <environment>

   You will be prompted to confirm that you want to proceed.

#. If the installation is using a dynamically-assigned IP address, you will need to set up the A record (and AAAA record if using IPv6) in DNS once that address has been assigned.

   Wait until the ``ingress-nginx`` application has been installed, which happens after Argo CD has been installed but before most applications are synced.
   Then, wait for it to be assigned an external IP address.
   Obtain that IP address with :command:`kubectl get -n ingress-nginx service` (look for the external IP).
   Then, set the A record in DNS for your environment to that address.

   For installations that are intended to be long-lived and that can reliably request the same address, add that IP address to the :file:`values-{environment}.yaml` file in :file:`applications/ingress-nginx` for your environment.
   The setting to use is ``ingress-nginx.controller.service.loadBalancerIP``.
   This ensures that ingress-nginx will always request that address.

#. If you are deploying on Google Cloud Platform, consider converting the dynamically-assigned IP address to a static IP.
   You can do this in the GCP console under :menuselection:`VPC Network -> IP addresses`.

#. Debug any problems during installation.
   The most common source of problems are errors or missing configuration in the :file:`values-{environment}.yaml` files you created for each application.
   You can safely run the installer repeatedly as you debug and fix issues.

Using a Vault token rather than AppRole
=======================================

The default and recommended installation approach is to use a Vault AppRole for vault-secrets-operator to authenticate to Vault.
However, using a read-only Vault token is still supported.

To use a Vault token instead of an AppRole, create an appropriate read-only token with access to the Vault path configured in :file:`enviroments/values-{environment}.yaml` for your environment.
Skip step 1 in the normal installation process, since you don't need to create an AppRole.
In step 2, set ``VAULT_TOKEN`` to the read-only token and do not set ``VAULT_ROLE_ID`` or ``VAULT_SECRET_ID``.
Then continue the regular installation process.

Troubleshooting tools
=====================

The tools to use for troubleshooting will vary depending on how far the installer has gotten.

- If something fails before Argo CD is installed, you will need to use :command:`kubectl` to look around in Kubernetes, retrieve logs, and look at error messages.

- If Argo CD is installed and working, but ingress-nginx fails, you can additionally use the :command:`argocd` command-line tool.
  The installer will have created login credentials for Argo CD as the admin user for you, so you shouldn't need to do that again.
  Pass the flags ``--port-forward --port-forward-namespace argocd`` to :command:`argocd` to proxy to the Argo CD server without needing to have the ingress working.

- If the ingress was successfully installed and you've created the DNS record for your environment, you can use the Argo CD web UI the same as you would with a fully-installed cluster.
  If your Argo CD authentication configuration is working (see :doc:`/applications/argocd/authentication`), you can log in as you normally would.
  If it is not, you will need to use the admin password.
  You can get this from Vault in the ``admin.plaintext_password`` key of the ``argocd`` secret.
