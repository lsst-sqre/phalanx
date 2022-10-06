#######################################
Deploying from a branch for development
#######################################

When developing services and their :doc:`Helm charts </service-guide/service-chart-architecture>`, it's useful to temporarily deploy from a branch of Phalanx on :doc:`designated development environments </ops/environments/index>` before merging to Phalanx's default branch.

Some use cases include:

- Testing that a new or updated Helm chart works in a higher-fidelity environment than the Minikube GitHub Actions CI cluster.
- Testing how a new or updated service interacts with other deployed services and cluster infrastructure like databases.

Through this process it is possible to develop a service in a fairly tight loop, though it's best to augment this practice with unit tests within the service's codebase.

.. seealso::

   This page focuses on using a development environment to iteratively develop and test changes to a service, ultimately yielding a service upgrade in Phalanx.
   You can achieve the same result, without the iterative deployment testing, following the steps in :doc:`upgrade`.

.. _deploy-branch-prep:

Preparing and pushing a branch
==============================

Start by creating a branch of the `phalanx repository`_ and editing your service.

You can make many types of edits to the service.
The most straightforward changes are updates to your service's Docker images or the Helm sub-charts the service depends on.
See :doc:`upgrade`.
You can also make changes to the Helm values by editing the service's defaults in its ``values.yaml`` file, or the values for the development environment in the corresponding ``values-<environment>.yaml`` file.
Finally, you can also make changes to the Helm templates for Kubernetes resources.

Commit your changes and push your branch to GitHub.
Throughout this process, you can continue to commit changes and push updates to your branch to GitHub.

.. tip::

   In a development environment it's useful to force Kubernetes to pull the service's Docker images every time a Pod_ starts up.
   This way you can push edits to the Docker images with a specific development tag [1]_ and then have your test deployment use those updated images.
   This setting is controlled by the ``imagePullPolicy`` key in Deployment_ resources (and specifically their Pods_).
   In typical service Helm charts the image pull policy is accessible from Helm values.
   In the service's values file for the development environment, set this pull policy to ``Always``:

   .. code-block:: yaml
      :caption: services/<service>/values-<environment>.yaml

      image:
        pullPolicy: Always

   Consult the Helm values documentation for your service for details.

   .. [1] SQuaRE Docker images are tagged with the Git branch or tag they are built from, with a typical branch build being tagged as ``tickets-DM-00000``.

Switching the Argo CD Application to sync the branch
====================================================

By default, Argo CD syncs your service from the default branch (``master``) of the `phalanx repository`_.
Change the service in Argo CD to instead sync from the branch you've pushed to GitHub:

1. Open your service's page in your environment's Argo CD UI.
   Generally the URL path for this page, relative to the environment's domain, is ``/argo-cd/applications/<service>``.

2. Click on the resource of type ``Application``.
   In the tree view this is the root node.

   .. image:: argocd-application.jpg

3. Click on the :guilabel:`Edit` button in the :guilabel:`Summary` pane.

   .. image:: application-edit-button.jpg

4. Edit the application to sync from your branch:

   1. Edit the :guilabel:`Target revision` field and enter your branch's name.
   2. Finally, click on the :guilabel:`Save` button.

   .. image:: application-revision-edit.jpg

5. In the service's page in Argo CD, click on the :guilabel:`Sync` button to redeploy the service from your branch.

   .. image:: sync-button.jpg

Updating the service's Helm chart
=================================

While your service is in active development, you may need to update its Helm chart and corresponding Kubernetes resources.
There are two ways of approaching these updates.

.. _updating-resources-in-argo-cd:

Editing resources directly in Argo CD
-------------------------------------

The fastest method for trying out changes to Kubernetes resources is to directly edit those resources in the Argo CD UI.
In your service's Argo CD page you can click on a specific resource (such as a ConfigMap_ or Deployment_) and click the :guilabel:`Edit` button on the live manifest.
Make your changes, then click :guilabel:`Save`.

Your application should show as out of sync.
Click the :guilabel:`Sync` button to redeploy the resources to the Kubernetes cluster.

Note that some changes won't affect a running deployment.
In some cases you many also need to restart Pods_ in Deployments_ to see changes take affect.
See :ref:`branch-deploy-restart`.

.. important::

   Edits to resources via the Argo CD UI are temporary.
   To make permanent changes, you need to edit the service's Helm chart in the `phalanx repository`_.

.. _updating-and-resyncing-from-branch:

Updating and resyncing from the branch
--------------------------------------

When you have edited your service's Helm chart in your development branch of the `phalanx repository`_, you need to sync those changes to Kubernetes.

Argo CD generally refreshes automatically.
If you have pushed your branch to GitHub and Argo CD doesn't show that your application is out-of-sync, you can click the :guilabel:`Refresh` button on your service's Argo CD page.

When your service shows an out-of-sync status, you can click the :guilabel:`Sync` button on your service's Argo CD page.
When individual services are synchronized their status changes from yellow to green.

In some cases you many also need to restart Pods_ in Deployments_ to see changes take affect.
See :ref:`branch-deploy-restart`.

Refreshing a deployment's Docker images
=======================================

Besides developing the service's Helm chart, you can also test branch builds of your service's Docker images inside Deployment_ resources.

To start, ensure that the Deployment_ is using development builds of your service's Docker images.
The best way to do this is to edit the service's Helm chart for the service in the development environment and to :ref:`sync those changes <updating-and-resyncing-from-branch>`.
For many services you can set the ``appVersion`` in the field in the service's ``Chart.yaml`` file to the name of the development Docker tag (see also :doc:`upgrade`).

You should also ensure that the Deployment_ is always pulling new images, rather than caching them, by setting the ``imagePullPolicy`` to ``Always``.
This is covered in :ref:`deploy-branch-prep`.

When new Docker images for your services are available with the corresponding branch tag from a container repository, you will need to restart the deployments using those images. See :ref:`branch-deploy-restart`.

.. _branch-deploy-restart:

Restarting a Deployment
=======================

Some changes won't affect a running Deployment_.
For example, many Deployments_ only read ConfigMap_ or Secret_ resources when Pods_ initially start up.
To realize an update, you'll see to restart the Pods_ in Deployments_.

To restart a Deployment_, find the Deployment_ resources in your service's Argo CD page, click on the three-vertical-dots icon, and select :guilabel:`Restart` from the menu.
New pods will appear while old pods will shut down.

.. figure:: restart-deployment.png
   :alt: Screenshot showing a Deployment in the Argo CD with its drop down menu, highlighting the Restart item.

   The Deployment drop-down menu for accessing
   Click on the three-vertical-dots to open the drop-down menu for a Deployment resource.
   Select the :guilabel:`Restart` item to restart the deployment.

If the new pods fail to start up, they will show a "crash-loop backoff" status and the old pods will continue to operate.
You'll need to resolve the error with changes to the service's Docker image and/or Helm charts.
After making fixes, you may need to restart the Deployment again.

Merging and switching the Argo CD Application to the default branch
===================================================================

Once development and testing is complete, you should submit the pull request for review following the `Data Management workflow guide`_.
Once your branch is merged, remember to reset your service's Argo CD ``Application`` resource to point back to the default branch (currently ``master``).

1. Open your service's page in your environment's Argo CD UI.
   Generally the URL path for this page, relative to the environment's domain, is ``argo-cd/applications/<service name>``.

2. Click on the resource of type ``Application``.
   In the tree view this is the root node.

3. Click on the :guilabel:`Edit` button in the :guilabel:`Summary` pane:

   - Edit the :guilabel:`Target revision` field back to the default branch (``master``).
   - Finally, click on the :guilabel:`Save` button.

4. In the service's page in Argo CD, click on the :guilabel:`Sync` button to redeploy the service from the default branch.

Next steps
==========

Follow this page, you have iterated on the development of your service and ultimately upgraded that service in a development environment.
The next step is to roll out this change to other environments.
For details, see :doc:`/ops/sync-argo-cd`.
