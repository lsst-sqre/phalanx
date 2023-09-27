.. px-app:: onepassword-connect-dev

####################################################
onepassword-connect-dev — 1Password API server (dev)
####################################################

1Password Connect provides API access to a 1Password vault.
It is used to provide the API for Phalanx integration with 1Password as a source of static secrets.

Each instance of the upstream 1Password Connect chart provides an API server for a single 1Password vault.
We want to use one vault per SQuaRE-managed Phalanx environment to ensure isolation of secrets between environments.
The Phalanx onepassword-connect applications therefore instantiate the upstream chart multiple times, one for each vault we are providing access to.

Unfortunately, because dependencies and their aliases can't be conditional on :file:`values.yaml` settings, that means the set of 1Password Connect servers deployed on roundtable-dev have to be a separate application from the ones deployed on roundtable.
This application is the roundtable-dev set of 1Password Connect API servers.
These provide access to the vaults for development and test environments.

.. jinja:: onepassword-connect-dev
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
