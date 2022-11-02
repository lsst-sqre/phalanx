.. px-app-bootstrap:: gafaelfawr

########################
Bootstrapping Gafaelfawr
########################

The primary documentation for configuring Gafaelfawr for a new environment is the `Gafaelfawr user guide <https://gafaelfawr.lsst.io/user-guide/index.html>`__.
That guide should provide most of the information required to write the ``values-<environment>.yaml`` file for Gafaelfawr for a new environment.

As described there, the primary configuration you will need to do is to choose between GitHub, CILogon, and a local OpenID Connect identity provider as a source of authentication.
If you choose an identity provider other than GitHub, you will then also have to decide how to retrieve user identity information such as full name, email address, UID, GID, and group membership.

:dmtn:`225` is a useful reference for user identity information sources for current Science Platform environments.
It may be helpful as a model for deciding policy for new environments.

You will also need to assign scopes to users based on either their group membership (for CILogon and local identity providers) or their GitHub team membership.
This is done with the ``config.groupMapping`` setting in ``values-<environment>.yaml``.

See :dmtn:`235` for a list of scopes used by the Science Platform.
You will need to assign all of them except ``admin:token`` and ``user:token``, which are handled internally by Gafaelfawr.

For ``admin:token``, ensure that the list of usernames in ``config.initialAdmins`` is correct before you start Gafaelfawr for the first time.
Otherwise, you will need to add admins later via the Gafaelfawr API.

If you run into authentication problems after installing your new environment, see :doc:`troubleshoot`.
