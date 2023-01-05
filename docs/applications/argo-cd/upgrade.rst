.. px-app-upgrade:: argocd

#################
Upgrading Argo CD
#################

This page provides upgrade procedures for the :px-app:`argocd` application.

.. warning::

   Do not use the `documented Argo CD upgrade method <https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/overview/>`__ that uses ``kubectl apply``.
   This will not work properly when Argo CD is installed via Helm, as it is in Phalanx.

Automatic upgrades
==================

Normally, you can let Argo CD upgrade itself (see `Manage Argo CD Using Argo CD <https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#manage-argo-cd-using-argo-cd>`__).
The upgrade will appear to proceed up to a point and then will apparently stall when the frontend pod is restarted.
When that happens, wait a minute or two and reload the page.
You should be presented with the login screen, can authenticate with GitHub or Google, and then will see the completed upgrade.

In some cases after an upgrade, Argo CD will claim that syncing itself failed.
This is usually a spurious failure caused by the controller restarting due to the upgrade.
Simply sync Argo CD again to resolve the error state.

If the upgrade results in a non-working Argo CD, often you can get it back to a working state by selectively downgrading the failed component using ``kubectl edit`` on the relevant ``Deployment`` resource.
This is particularly true if Dex failed (which will cause errors when logging in), since it is largely independent of the rest of Argo CD.

Manual upgrade process
======================

Only use this process if the automatic upgrade failed or if there are documented serious problems with automatic upgrades.

#. Determine the current version of Argo CD.

   The easiest way to do this is to go to the ``/argo-cd`` route and look at the version number in the top left sidebar.
   Ignore the hash after the ``+`` sign; the part before that is the version number.

#. Ensure your default ``kubectl`` context is the cluster you want to upgrade.
   Check your current context with ``kubectl config current-context`` and switch as necessary with ``kubectl config use-context``.

#. Back up the Argo CD configuration:

   .. code-block:: sh

      chmod 644 ~/.kube/config
      docker run -v ~/.kube:/home/argocd/.kube --rm \
        argoproj/argocd:$VERSION argocd-util export -n argocd > backup.yaml
      chmod 600 ~/.kube/config

   You have to temporarily make your ``kubectl`` configuration file world-readable so that the Argo CD Docker image can use your credentials.
   Do this on a private system with no other users.
   Replace ``$VERSION`` with the version of Argo CD as discovered above.
   The version will begin with a ``v``.

   This is taken from the `Argo CD disaster recovery documentation <https://argo-cd.readthedocs.io/en/stable/operator-manual/disaster_recovery/>`__ with the addition of the namespace flag.

   The backup will not be needed if all goes well.

#. Determine the new version of the Argo CD Helm chart (**not** Argo CD itself) to which you will be upgrading:

   .. code-block:: sh

      helm repo add argo https://argoproj.github.io/argo-helm
      helm repo update
      helm search repo argo-cd

   Note the chart version for ``argo/argo-cd``.

#. Upgrade Argo CD using Helm.
   Check out the `Phalanx repository`_ first.

   .. code-block:: sh

      cd phalanx/installer
      helm upgrade --install argocd argo/argo-cd --version $VERSION \
        --values argo-cd-values.yaml --namespace argocd --wait --timeout 900s

   Replace ``$VERSION`` with the Helm chart version (**not** the Argo CD application version) that you want to install.

If all goes well, you can now view the UI at ``/argo-cd`` and confirm that everything still looks correct.

Recovering from a botched upgrade
---------------------------------

If everything goes horribly wrong, you can remove Argo CD entirely and the restore it from the backup that you took.
To do this, first drop the Argo CD namespace:

.. code-block:: sh

   kubectl delete namespace argocd

You will then need to manually remove the finalizers for all the Argo CD application resources in order for the namespace deletion to succeed.
The following instructions are taken from `kubernetes/kubernetes#77086 <https://github.com/kubernetes/kubernetes/issues/77086>`__:

.. code-block:: sh

   kubectl api-resources --verbs=list --namespaced -o name \
     | xargs -n 1 kubectl get --show-kind --ignore-not-found -n argocd

This will show all resources that need manual attention.
It should only be Argo CD ``Application`` and ``AppProject`` resources.
For each resource, edit it with ``kubectl edit -n argocd`` and delete the finalizer.
As you save each resource, its deletion should succeed.
By the end, the namespace should successfully finish deletion.
You can then recreate the namespace, reinstall Argo CD, and restore the backup:

.. code-block:: sh

   kubectl create namespace argocd
   cd phalanx/installer
   helm upgrade --install argocd argo/argo-cd --version $HELM_VERSION \
     --values argo-cd-values.yaml --namespace argocd --wait --timeout 900s
   chmod 644 ~/.kube/config
   docker run -i -v ~/.kube:/home/argocd/.kube --rm \
     argoproj/argocd:$VERSION argocd-util import -n argocd - < backup.yaml
   chmod 600 ~/.kube/config

Replace ``$HELM_VERSION`` with the version of the Helm chart you want to use and ``$VERSION`` with the corresponding Argo CD version (as shown via ``helm search repo``).

This should hopefully restore Argo CD to a working state.
If it doesn't, you'll need to reinstall it using the more extended process used by the cluster installer.
See `installer/install.sh <https://github.com/lsst-sqre/phalanx/blob/main/installer/install.sh>`__ for the commands to run.
