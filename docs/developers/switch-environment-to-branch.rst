#################################
Switch an environment to a branch
#################################

If an application is already deployed in an environment, you can easily test changes from a Phalanx PR branch before merging it.
This is documented in :doc:`deploy-from-a-branch`.

If the application is not already deployed to a given environment, the Argo CD application for it will not exist and that process will not work.
In this case, deploying your application from a branch requires the additional step of switching the Argo CD "app of apps" application to your branch first.

First, add your application to an environment on a Phalanx PR branch and push that branch to https://github.com/lsst-sqre/phalanx.
Do not use a GitHub fork; the steps below require that your change be on a branch in that repository.

Then, take the following steps:

#. Go to the Argo CD dashboard for the environent where you want to test your application, and locate the "app of apps" application.
   Normally this is named ``science-platform``, but it is named ``roundtable`` on Roundtable clusters and may have other names on other clusters.
   This is the Argo CD application that manages all of the namespaces and other Argo CD applications.
   Click on that application to bring up its Argo CD page.

#. Click on the :guilabel:`Details` button in the top bar.
   Then click on :guilabel:`Edit`.

#. Change the branch name under :guilabel:`Target Revision` to the name of your PR branch.
   It previously should have been set to ``main``.
   Click :guilabel:`Save`.

#. Click on the :guilabel:`Sync` button in the top bar.
   Under :guilabel:`Synchronize Resources`, click on :guilabel:`none` to not sync anything by default.
   Then, select the checkboxes for only the namespace and the application resource for your application.
   When you've configured Argo CD to sync only those two resources, click :guilabel:`Synchronize`.

#. You could now continue with testing your application, but before you do, click on the :guilabel:`Details` button in the top bar again, click on :guilabel:`Edit`, and change the branch name under :guilabel:`Target Revision` back to ``main``.
   Click :guilabel:`Save`.
   This will not delete your application again until someone syncs the "app of apps" application, so you can still continue with your testing.
   It will restore the previous state of the "app of apps" so that other people can sync changes, and it will show your application and namespace as out of date until you merge your PR.
   This is the desired behavior; we want temporary changes like this for testing should show as out of date so that we can see at a glance that we're running unmerged changes.

Next steps
==========

- Test your application by deploying it from a branch: :doc:`deploy-from-a-branch`
