##########################
Add a new Gafaelfawr scope
##########################

In order for Gafaelfawr to apply authorization rules, there has to be a scope that matches the granularity of access to be granted.
Rarely, it may be necessary to add a new scope to avoid granting too much access.

.. warning::

   Avoid adding new scopes whenever possible, since a large number of scopes becomes unwieldy.
   Most group-based access control decisions should be made inside applications rather than by using Gafaelfawr scopes.
   Read the cautions in :dmtn:`235` before proceeding.

Adding a new scope requires the following steps:

#. Add the new scope and its description to ``config.knownScopes`` in :file:`applications/gafaelfawr/values.yaml`.
   It is possible to add the scope only in specific environments, but we prefer to keep the list of scopes the same in all environments since it makes writing Phalanx Helm charts easier.

#. If necessary (if there is no existing group that can be used for this purpose), create a new group containing the specific people who will be granted the new scope.
   How to do this will depend on the source of groups for every affected environment.
   For example, for environments that use COmanage, do this in the corresponding COmanage instance for each environment.
   For environments that use GitHub, add people to an appropriate team.

#. By default, no one will receive the new scope.
   For every environment where the application using the new scope will be deployed, add a group mapping rule to ``config.groupMappings`` in :file:`applications/gafaelfawr/values-{environment}.yaml`.
   Yes, this is tedious and requires modifying lots of environments in the common case.
   This helps discourage you from adding new scopes unnecessarily.

#. Update the ``GafaelfawrIngress`` resource in the applications that will use the new scope to require it instead of whatever scope they were using before.

#. Update :dmtn:`235` to document the new scope in more detail.

#. When syncing applications in each environment to apply this change, sync the ``gafaelfawr`` application first before syncing any application that wants to start using the scope for access control.

Be aware that, after Gafaelfawr has been synced, users will have to log out and log back in to get their new scope.
Users with existing sessions will not have that scope, even if they are eligible for it based on their group memberships, and thus will be denied access to ingresses that require it until they log out and back in.
