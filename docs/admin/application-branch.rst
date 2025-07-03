####################################
Running an application from a branch
####################################

The Argo CD app-of-apps that installs all the Argo CD applications expected to run in a given environment by default points all of them at the Git revision ``targetRevision``, configured in :file:`environments/values-{environment}.yaml`.
The default is ``main``, which points all applications at the ``main`` branch of Phalanx.

This is the recommended configuration and should be used for the vast majority of environments.
In most cases, running an application from a branch should be short-lived and used only for :doc:`testing work in progress </developers/deploy-from-a-branch>`.
When the testing is complete, the application should be pointed back to the ``main`` branch.

However, sometimes there is a need to run specific applications from a branch for an extended period of time.
Examples include staging major upgrades in a testing environment for an extended period, or pointing some production environments at a stable branch of an application to postpone a major upgrade until a scheduled upgrade window.

To support this, the target revision of specific Argo CD applications can be overridden in the :file:`environments/values-{environment}.yaml` files with the ``revisions`` key.
This key contains a mapping of application names to target revisions (normally Git branches but any Git revision may be used).
When the Argo CD app-of-apps is then synced, the application will be configured to point to that revision for its Helm chart and values files.

For example, to deploy the :px-app:`strimzi` application from the ``renovate/strimzi-kafka-operator-0.x`` branch on the :px-env:`idfdev` environment, add the following configuration:

.. code-block:: yaml
   :caption: environments/values-idfdev.yaml

   revisions:
     strimzi: "renovate/strimzi-kafka-operator-0.x"

When the app-of-apps for :px-env:`idfdev` (``science-platform``) is synced, the :px-app:`strimzi` application will be pointed at that branch.
When that branch has been tested and merged, delete this configuration and sync ``science-platform`` again to move the application back to the default ``main`` branch.

.. warning::

   Overriding the default revision for an application should only be used in rare circumstances where extended testing or upgrade postponement is required.
   Mixing branches in this way dramatically increases the complexity and maintenance cost of Phalanx, and exceessive use of this feature will cause confusion and wasted effort.

   Normally, applications should be moved to branches manually following the instructions in :doc:`/developers/deploy-from-a-branch`, and the out-of-date status of the app-of-apps should be used as a reminder that there is pending work that needs to be completed and merged.
   Whenever possible, try to merge all work to ``main`` once it is tested and upgrade all environments to the current ``main`` branch during their patch windows.
