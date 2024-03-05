##############################################
Enable 1Password Connect for a new environment
##############################################

SQuaRE-managed Phalanx deployments keep their static secrets in 1Password.
This means that each Phalanx environment run by SQuaRE needs to have a corresponding 1Password vault, and a 1Password Connect server that provides access to that vault.
One 1Password Connect server can provide access to multiple vaults using multiple separate tokens, each of which is scoped to only one vault.

SQuaRE runs two 1Password Connect servers, one in the :px-env:`roundtable-dev <roundtable-dev>` environment for development environments and one in the :px-env:`roundtable-prod <roundtable-prod>` environment for production environemnts.

This document describes how to enable the 1Password Connect server to serve the vault for a new environment.

.. note::

   These instructions only apply to SQuaRE-managed Phalanx environments.
   You can use them as a model for how to use 1Password as a static secrets source with a different 1Password account, but some modifications will be required.

.. _onepassword-add-prerequisites:

Prerequistes
============

Every environment must have a separate 1Password vault in the **LSST IT** 1Password account.
The vault for the environment should be named ``RSP <fqdn>`` where ``<fqdn>`` is the top-level FQDN for that environment.
(In hindsight the vaults should be named after the short environment names used in Phalanx, but sadly that's not what we did.)

When following these instructions, you will be modifying a `Secrets Automation workflow <https://developer.1password.com/docs/connect/get-started/>`__.
You will need to have permissions to modify the workflow for the 1Password Connet server that will be serving your environment.

Process
========

In the following steps, you'll change the permissions of the 1Password Connect server to add the new 1Password vault for your environment and create a new token with access to that vault.

#. Log on to the 1Password UI via a web browser.

#. Click on :menuselection:`Integrations` in the right sidebar under **LSST IT**.

#. Click on the Secrets Management workflow for the 1Password Connect server that will be serving this environment.

#. Next to :guilabel:`Vaults`, click on :guilabel:`Manage`.
   Select the vault for the environment that you're adding, in addition to the existing vaults.
   Click :guilabel:`Update Vaults`.

#. Next to :guilabel:`Access Tokens`, click on :guilabel:`New Token`.

#. Under :guilabel:`Environment Name`, enter the same name as the 1Password vault name for your environment.
   Then, click :guilabel:`Choose Vaults` and select the corresponding vault (and only that one).
   Click :guilabel:`Issue Token` to continue.

#. Next to the access token, click on the clipboard icon to copy the token to the clipboard.
   Then, click on :guilabel:`View Details` to continue.

#. Go back to home by clicking on the icon on the upper left.
   Go to the SQuaRE vault, find the ``RSP 1Password tokens``, and edit it.
   Add the token to that item as another key/value pair, where the key is the short name of the enviroment.
   Mark the value as a password.

#. Modify :file:`environments/values-{environment}.yaml` to add the configuration for the 1Password Connect server:

   .. code-block:: yaml

      onepassword:
        connectUrl: "https://roundtable-dev.lsst.cloud/1password"
        vaultTitle: "RSP <fqdn>"

   The ``connectUrl`` will be either ``https://roundtable-dev.lsst.cloud/1password`` (development environments) or ``https://roundtable.lsst.cloud/1password`` (production environments) for SQuaRE-run environments.
   ``vaultTitle`` should be set to the name of the 1Password vault for the environment (see :ref:`onepassword-add-prerequisites`).

Next steps
==========

You have now confirmed that 1Password is set up for your environment.

- If you are migrating from the old secrets management system, perform the other steps now: :doc:`/admin/migrating-secrets`
- If you are setting up a new environment, start populating the 1Password vault with static secrets for the applications running in that environment: :doc:`/admin/add-new-secret`
