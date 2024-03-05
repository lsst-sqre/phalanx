.. px-app-bootstrap:: gafaelfawr

########################
Bootstrapping Gafaelfawr
########################

The primary documentation for configuring Gafaelfawr for a new environment is the `Gafaelfawr user guide <https://gafaelfawr.lsst.io/user-guide/index.html>`__.
That guide should provide most of the information required to write the ``values-<environment>.yaml`` file for Gafaelfawr for a new environment.

For a new environment, it's worth reading all of the user guide.
There are a lot of configuration decisions you will need to make.

If you run into authentication problems after installing your new environment, see :doc:`troubleshoot`.

Choose an identity provider
===========================

As described there, the primary configuration you will need to do is to choose between GitHub, CILogon, and a local OpenID Connect identity provider as a source of authentication.
If you choose an identity provider other than GitHub, you will then also have to decide how to retrieve user identity information such as full name, email address, UID, GID, and group membership.

:dmtn:`225` is a useful reference for user identity information sources for current Science Platform environments.
It may be helpful as a model for deciding policy for new environments.

If you choose GitHub as the identity provider, you may need to configure the privacy settings of organizations used for user groups.
See :doc:`github-organizations` for more details.

Assign scopes and admins
========================

You will also need to assign scopes to users based on either their group membership (for CILogon and local identity providers) or their GitHub team membership.
This is done with the ``config.groupMapping`` setting in ``values-<environment>.yaml``.

See :dmtn:`235` for a list of scopes used by the Science Platform.
You will need to assign all of them except ``admin:token`` and ``user:token``, which are handled internally by Gafaelfawr.

For ``admin:token``, ensure that the list of usernames in ``config.initialAdmins`` is correct before you start Gafaelfawr for the first time.
Otherwise, you will need to add admins later via the Gafaelfawr API.

Enable database schema initialization
=====================================

When you are bootstrapping the new environment, set ``config.updateSchema`` to true in :file:`values-{environment}.yaml` for the ``gafaelfawr`` application.
This tells Helm to use a pre-install hook to initialize the database before installing other Gafaelfawr resources.
Remove this setting once you have successfully bootstrapped the environment.

See :ref:`gafaelfawr-db-init` for more details.
