#####################################
Blocking spawns of new user notebooks
#####################################

In some cases, we may want to block spawns of new user Nublado pods.
For example, if the system is very overloaded, we may want to temporarily disable new pod creation.
We may also want to disable spawning of new pods before the start of planned maintenance.

Blocking spawns via quota
=========================

Gafaelfawr_ tracks user quotas, including notebook quotas.
Part of the user notebook quota is a boolean flag, ``spawn``, that specifies whether that user can spawn new labs.
Lab spawns for either a group or for all users by default can be disabled by setting that flag to false.

This can be done via the user quota settings in the :file:`values-{environment}.yaml` file for Gafaelfawr for a given environment and applied with Phalanx (see `the Gafaelfawr quota documentation <https://gafaelfawr.lsst.io/user-guide/helm.html#quotas>`__), but usually one does not want to disable spawning permanently.
It's more common to want to disable spawns temporarily.

To do this, an environment administrator can use a Gafaelfawr quota override.
This is a separate, temporary Gafaelfawr quota configuration that overrides the default quotas if it applies.

To set a quota override, first create a user token with ``admin:token`` scope.
This token has full administrative access to the Phalanx environment, so treat it with caution.

Then, using that token, run a command such as the following:

.. prompt:: bash

   curl -X PUT -H 'Authorization: bearer <token>' \
       -H 'Content-Type: application/json' \
       -d '{"default": {"notebook": {"cpu": 0, "memory": 0, "spawn": false}}}' \
       https://<base-url>/auth/api/v1/quota-overrides

This sets an override notebook quota that disables spawning for all users.

To allow members of an admin group to spawn notebooks anyway, add that group to the ``bypass`` key.
For example, the ``-d`` argument to :command:`curl` might look like this:

.. code-block:: json

   {"bypass": ["g_admins"], "default": {"notebook": {"cpu": 0, "memory": 0, "spawn": false}}}

In this case, all members of ``g_admins`` will ignore all quotas, including the notebook quota that disables spawns (and also any default quotas configured elsewhere).

Alternately, you can block notebook spawns for only members of a specific group with JSON such as this:

.. code-block:: json

   {"default": {}, "groups": {"g_users": {"notebook": {"cpu": 0, "memory": 0, "spawn": false}}}}

This will disable spawning only for members of the ``g_users`` group.

Blocking spawns by stopping JupyterHub
======================================

A more comprehensive way to block all notebook spawns is to stop JupyterHub entirely.
You can do this by going into Argo CD, choosing the ``nublado`` application, and then deleting the Kubernetes deployment named ``hub``.

This will prevent anyone from spawning notebooks or interacting with JupyterHub, but it will always affect all users with no bypass mechanism.
It will also break other functionality, such as returning to an already-running lab, and may cause problems for running user labs since they are no longer able to contact JupyterHub.

This should therefore only be used in emergencies or when the entire Nublado environment is being brought down.
Use quota overrides instead for finer-grained control of spawning.
