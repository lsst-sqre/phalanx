.. px-app-bootstrap:: argocd

#####################
Bootstrapping Argo CD
#####################

Authentication
==============

Initial installation of the Rubin Science Platform is done using Argo CD and a static password for the ``admin`` account.
You can then log on to the ``admin`` account using that password to manage the resulting environment.
The password is available as the ``admin.plaintext_password`` key in Vault secret for the ``argocd`` application, and in the ``Secret`` resource named ``argocd-secret`` in the ``argocd`` namespace after installation of the environment.

As part of bootstrapping a new environment, you should also configure per-user authentication.
To do this, follow the instructions in :doc:`authentication`.

Once the environment has been installed, switch to using per-user authentication for all routine operations, and save the ``admin`` account only for emergency situations, such as some problem that breaks per-user authentication.

Access control
==============

When you followed the instructions in :doc:`authentication`, you set up ``role:admin`` access to Argo CD for a group or list of users.

If the only people who need to manage applications in the environment are those administrators, you don't need to do any further configuration.
If other people need to view or modify some Argo CD applications, you will need to configure up Argo CD RBAC (role-based access control).

Built-in roles
--------------

Argo CD supports two built-in roles, the first of which you configured when following the steps in :doc:`authentication`:

``role:admin``
    Full read/write access to everything managed by Argo CD.

``role:readonly``
    Read-only access to everything, but no write access.

You can add additional users or groups to these roles using ``g`` lines in the ``argo-cd.configs.cm.rbac."policy.csv"`` key in :file:`values-{environment}.yaml`.

Custom roles
------------

If you want to give some users access to change some Argo CD applications but not others, you will need to define a custom role and then assign it to users or groups.

All applications in Argo CD are assigned to a project.
The list of projects are the top-level divisions in :doc:`/applications/index`.
The primary purpose of these projects is for access control.
The ``infrastructure`` project, in particular, holds the critical Phalanx infrastructure that application developers should not need to change and that runs the highest risk of breaking the environment in a way that would require Kubernetes-level intervention.

A common RBAC pattern is therefore to set up a ``role:developer`` role that has write access to all applications except those in the ``infrastructure`` project.
To create this role, add the following lines to the top of the ``policy.csv`` in :file:`values-{environment}.yaml` for your environment::

   p, role:developer, applications, *, */*, allow
   p, role:developer, applications, get, infrastructure/*, allow
   p, role:developer, applications, create, infrastructure/*, deny
   p, role:developer, applications, update, infrastructure/*, deny
   p, role:developer, applications, delete, infrastructure/*, deny
   p, role:developer, applications, sync, infrastructure/*, deny
   p, role:developer, applications, override, infrastructure/*, deny
   p, role:developer, applications, action/*, infrastructure/*, deny

You can then assign ``role:developer`` to users or groups in exactly the same way as the built-in ``role:admin`` and ``role:readonly`` roles.

This same approach can be used to restrict access to other Argo CD projects (such as ``telescope``).
Or, alternately, you can grant a role write access to only one Argo CD project and read access to everything else with a role definition like::

   p, role:rsp, applications, get, */*, allow
   p, role:rsp, applications, *, rsp/*, allow

More complicated rules are possible.
See the `Argo CD RBAC documentation <https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/>`__ for the details.
