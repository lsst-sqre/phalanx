############################
Managing the database schema
############################

Gafaelfawr uses Alembic_ to version the database schema.
No component of Gafaelfawr that may write to the database will start if the database schema is out of date.

.. _Alembic: https://alembic.sqlalchemy.org/en/latest/

Updating the database schema
============================

.. warning::

   Schema downgrades are not supported.
   Once you update the schema, you must run the new version of Gafaelfawr corresponding to that new database schema.
   If you have to revert to an older version of Gafaelfawr, you will have to restore the database or manually try to downgrade the schema.

   We therefore recommend that you test schema updates, and any new versions of Gafaelfawr that require them, in a development environment before upgrading a production deployment.
   You want to catch any blocking problems and ensure they are resolved before you update the production database schema.

To update the database schema of an existing Gafaelfawr installation, follow these steps:

#. Announce and schedule downtime, since updating the schema will break all Gafaelfawr-managed cluster authentication for a few minutes.
#. Set ``config.updateSchema`` to true in the :file:`values-{environment}.yaml` file for the ``gafaelfawr`` application for this environment.
#. In Argo CD for this Phalanx environment, stop all of the Gafaelfawr deployments.
   The easiest way to do that is to delete the deployment in Argo CD.
   Be sure to delete both the ``gafaelfawr`` and the ``gafaelfawr-operator`` deployments.
#. Sync the ``gafaelfawr`` application.
   This will use a Helm pre-upgrade hook to update the schema, and then will sync the rest of the Gafaelfawr application, including recreating the deployments that you deleted above.
#. Delete the ``config.updateSchema`` override in :file:`values-{environment}.yaml` to disable automatic schema updates again.
   Safely performing a schema update requires stopping Gafaelfawr first, so you do not want schema updates to be applied without human intervention.

At this point, the schema update should be complete.

You may wish to delete the extra Kubernetes resources used only by the schema update hook.
Argo CD will mark them with a small anchor or hook icon, and they will have ``schema-update`` in their names.
These resources don't cause any problems, but they add some clutter and Helm and Argo CD for some reason don't delete them automatically.

.. _gafaelfawr-db-init:

Initializing the database
=========================

Initializing an empty, new database with the Gafaelfawr database schema is very similar to updating the schema to a new revision.

#. Set ``config.updateSchema`` to true in the :file:`values-{environment}.yaml` file for the ``gafaelfawr`` application for this environment.
#. Sync the ``gafaelfawr`` application.
   This will use a Helm pre-install or pre-upgrade hook to initialize the database schema before installing the other Gafaelfawr Kubernetes resources.
#. Delete the ``config.updateSchema`` override in :file:`values-{environment}.yaml` to disable automatic schema updates again.
   Safely performing a schema update requires stopping Gafaelfawr first, so you do not want schema updates to be applied without human intervention.

As a special case, the :px-env:`minikube` environment always has ``config.updateSchema`` enabled since it is used for GitHub CI, where it is constantly installed with a new, empty database.
