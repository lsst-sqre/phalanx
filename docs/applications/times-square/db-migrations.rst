###################################
Managing database schema migrations
###################################

Times Square use Alembic_ to manage its SQLAlchemy-based relational database.
When a new version of Times Square is released that includes database schema changes, you will need to run the procedure described here.
Times Square checks if the database schema is consistent with the codebase when it starts up, making it impossible to run the application if the schema is out of date.

Upgrading the database schema
=============================

1. If Times Square is running in a production environment, schedule and announce downtime for Times Square.

2. Set ``config.updateSchema`` to true in the :file:`values-{environment}.yaml` file for the ``times-square`` application for this environment:

   .. code-block:: yaml
      :caption: applications/times-square/values-{environment}.yaml

      config:
        updateSchema: true

   Push these changes to GitHub on the branch that is deployed to the environment.

3. Stop the Times Square deployments by deleting the Kubernetes deployment for both the API service and the worker service in Argo CD.

4. Sync the Times Square application in Argo CD. This takes the follow actions:

   1. The ``times-square-schema-update`` Kubernetes Job runs as a Helm pre-upgrade hook.
   2. The Times Square API and worker deployments are recreated.

5. In Phalanx, reset the ``config.updateSchema`` value to false in the :file:`values-{environment}.yaml` file for the ``times-square`` application for this environment.

.. _Alembic: https://alembic.sqlalchemy.org/en/latest/
