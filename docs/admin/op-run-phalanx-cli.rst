###############################################
Run the phalanx CLI with secrets from 1Password
###############################################

The :command:`phalanx secrets` CLI uses ``OP_CONNECT_TOKEN`` and ``VAULT_TOKEN`` environment variables to access secrets in 1Password and Vault, respectively.
To conveniently and securely load these secrets, you can use the 1Password CLI in conjunction with ``.env`` files in the :file:`op` directory of the Phalanx repository.

.. note::

   This documentation is relevant to Phalanx environments managed by SQuaRE.

Set up
======

To use this technique, you need to have the 1Password CLI (:command:`op`) installed.
See the `1Password CLI documentation <https://developer.1password.com/docs/cli>`__ for installation instructions.

Next, ensure that you're signed into the 1Password Vault containing the Phalanx secrets:

.. prompt:: bash

   op signin --account lsstit

Change the account as needed for non-SQuaRE environments.

Run the phalanx CLI with 1Password secrets
==========================================

To run the phalanx CLI with secrets from 1Password, you can prefix the :command:`phalanx` command with :command:`op run`, as in:

.. prompt:: bash

   op run --env-file=op/<env>.env -- phalanx <command> <args>

For example:

.. prompt:: bash

   op run --env-file=op/idfprod.env -- phalanx secrets audit idfprod

The :file:`op/` directory contains a set of ``.env`` files, one for each environment.
Match the environment name in the ``.env`` file with the environment you are working with.
