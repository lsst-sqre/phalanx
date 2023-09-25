#################################
Syncing Argo CD in an environment
#################################

Phalanx enables environment administrators to roll out new and updated applications by synchronizing deployemnts in Kubernetes to the current HEAD of the `phalanx repository`_ using `Argo CD`_.
This page explains the key steps in this process for environment administrators.

.. important::

   Keep in mind that environments have specific upgrade windows and that application updates should be rolled out to environments in sequence to development and integration environments before production environments.
   See :doc:`upgrade-windows` for details.

Log into Argo CD for the environment
====================================

To access the Argo CD UI, go to the ``/argo-cd`` URL under the domain name of that deployment of the Rubin Science Platform.
See :doc:`/environments/index` for a list of Phalanx environments and direct links to their Argo CD pages.

Depending on the environment, you will need to authenticate with either GitHub, Google OAuth, CILogon, or another OAuth provider as relevant.
You can use the ``admin`` account and password, stored in 1Password for deployments managed by SQuaRE, in case of an emergency.

Sync the application
====================

Out-of-date applications will show as yellow in Argo CD.
Click on the application to see its current resources and more details about its status.
If the update was made recently, you may have to click :guilabel:`Refresh` first.

To review the changes before applying them, select :guilabel:`App Diff`.

To apply the changes, select :guilabel:`Sync`.

Once your Argo CD says you are green, then you are where you say you want to be.
If something happens to the cluster and its resources, Argo CD will let you know, even the action wasn't taken by Argo CD.

Revert to a previous configuration
==================================

To revert to a previous version of the application configuration, select :guilabel:`History and Rollback`, find the previous configuration to which you want to revert, and then click on the vertical three dots on the right side of the box for that version.
Select :guilabel:`Rollback` from the resulting menu.
