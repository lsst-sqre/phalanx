##################################
Add a new 1Password Connect server
##################################

This document describes how to set up a new 1Password Connect server to push secrets from 1Password to Vault for one or more Phalanx environments.

SQuaRE-run Phalanx environments already have 1Password Connect servers set up.
The one in the :px-env:`roundtable-dev <roundtable-dev>` environment serves the vaults for development environments, and one in the :px-env:`roundtable-prod <roundtable-prod>` environment serves the vaults for production environments.

When following these instructions, you will be creating a new `Secrets Automation workflow <https://developer.1password.com/docs/connect/get-started/>`__.
You will need to have permissions to create that workflow for the vault for your environment.

Create the workflow
===================

In the following steps, you will create a 1Password Secrets Automation workflow for the 1Password vault for your environment, and save the necessary secrets to another 1Password vault.

#. Log on to the 1Password UI via a web browser.

#. Click on :menuselection:`Integrations` in the right sidebar under **LSST IT**.

#. Click on the :guilabel:`Directory` tab at the top of the screen.

#. Under :guilabel:`Infrastructure Secrets Management` click on :guilabel:`Other`.

#. Click on :guilabel:`Create a Connect server`.

#. Under :guilabel:`Environment Name`, enter :samp:`RSP {environment}` where *environment* is the Phalanx environment in which this 1Password Connect server will be running (**not** the vaults that it will serve).
   Then, click :guilabel:`Choose Vaults` and select the vaults that should be accessible through this 1Password Connect server.
   Click :guilabel:`Add Enviroment` to continue.

#. Next, 1Password wants you to create an access token for at least one environment.
   This is the token that will be used by the Phalanx command-line tool to access secrets for that environment.
   It will have access to one and only one vault.

   Under :guilabel:`Token Name`, enter the name of the environment the token should have access to.
   Leave :guilabel:`Expires After` set to ``Never``.
   Click :guilabel:`Choose Vaults` and choose the vault corresponding to that environment.
   Click :guilabel:`Issue Token` to continue.

#. Next to the credentials file, click :guilabel:`Save in 1Password`, change the title to :samp:`1Password Connect credentials ({environment})` (with *environment* set to the environment in which the 1Password Connect server will be running), select the ``SQuaRE`` vault, and click :guilabel:`Save`.
   Then, next to the access token, click the clipboard icon to copy that token to the clipboard.

#. Click :guilabel:`View Details` to continue.
   Go back to home by clicking on the icon on the upper left.

#. Go to the SQuaRE vault, find the item ``RSP 1Password tokens``, and edit it.
   Add the token to that item as another key/value pair, where the key is the short name of the enviroment.
   Mark the value as a password.

#. Confirm that the new ``1Password Connect credentials`` item created two steps previous exists.
   You will need this when creating the 1Password Connect server.
   You can download it to your local system now if you wish.

Create the Phalanx configuration
================================

In the following steps, you'll deploy the new 1Password Connect server.

#. Download the file in the :samp:`1Password Connect credentials ({environment})` item in the SQuaRE vault.
   It will be named :file:`1password-credentials.json`.

#. Encode the contents of that file in base64.

   .. prompt:: bash

      base64 -w0 < 1password-credentials.json; echo ''

   This is the static secret required by the 1Password Connect server.

#. If you are following this process, you are presumably using 1Password to manage your static secrets.
   Go to the 1Password vault for the environment where the 1Password Connect server will be running.
   Create a new application secret item for the application ``onepassword-connect`` (see :ref:`dev-add-onepassword` for more details), and add a key named ``op-session`` whose value is the base64-encoded 1Password credentials.

#. Synchronize secrets for that environment following the instructions in :doc:`/admin/sync-secrets`.

.. note::

   That final step assumes that the 1Password Connect server for the environment where you're deploying a new 1Password Connect server is running elsewhere.
   In some cases, such as for the SQuaRE :px-env:`roundtable-prod <roundtable-prod>` and :px-env:`roundtable-dev <roundtable-dev>` environments, the 1Password Connect server for that environment runs in the environment itself.

   In this case, you won't be able to use :command:`phalanx secrets sync` because the 1Password Connect server it wants to use is the one you're trying to install.
   Instead, follow the :px-app-bootstrap:`bootstrapping instructions for onepassword-connect <onepassword-connect>`.
