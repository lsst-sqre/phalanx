#################
Upgrading Argo CD
#################

Automatic upgrades
==================

Normally, you can let Argo CD upgrade itself.
According to the documentation, this is not necessarily safe.
The developers recommend the manual process documented below instead.
However, it's much more convenient to do the upgrade through Argo CD and we have had good luck with it.
Just be aware that it's not entirely supported.

When performing the upgrade through Argo CD, it appears to be somewhat more reliable to use the following process rather than telling Argo CD to sync everything at once:

#. Sync everything except the deployments by unchecking them in the sync dialog
#. Sync the argocd-redis deployment and wait for it to be green
#. Sync the remaining deployments one at a time in the following order (the exact order probably doesn't matter, but this is what we've done):
   - ``argocd-application-controller``
   - ``argocd-server``
   - ``argocd-repo-server``
   - ``argocd-dex-server``

Manual upgrade process
======================

#. Determine the current version of Argo CD.
   The easiest way to do this is to go to the ``/argo-cd`` route and look at the version number in the top left sidebar.
   Ignore the hash after the ``+`` sign; the part before that is the version number.

#. Ensure your default ``kubectl`` context is the cluster you want to upgrade.
   Check your current context with ``kubectl config current-context`` and switch as necessary with ``kubectl config use-context``.

#. Back up the Argo CD configuration.

   .. code-block:: console

      $ chmod 644 ~/.kube/config
      $ docker run -v ~/.kube:/home/argocd/.kube --rm \
          argoproj/argocd:$VERSION argocd-util export -n argocd > backup.yaml
      $ chmod 600 ~/.kube/config

   You have to temporarily make your ``kubectl`` configuration file world-readable so that the Argo CD Docker image can use your credentials.
   Do this on a private system with no other users.
   Replace ``$VERSION`` with the version of Argo CD as discovered above.
   The version will begin with a ``v``.

   This is taken from the `Argo CD disaster recovery documentation <https://argoproj.github.io/argo-cd/operator-manual/disaster_recovery/>`__ with the addition of the namespace flag.

   The backup will not be needed if all goes well.

#. Determine the new version of the Argo CD Helm chart (**not** Argo CD itself) to which you will be upgrading.

   .. code-block:: console

      $ helm repo add argo https://argoproj.github.io/argo-helm
      $ helm repo update
      $ helm search repo argo-cd

   Note the chart version for ``argo/argo-cd``.

#. Upgrade Argo CD using Helm.
   Check out the `phalanx repository <https://github.com/lsst-sqre/phalanx>`_ first.

   .. code-block:: console

      $ cd phalanx/installer
      $ helm upgrade --install argocd argo/argo-cd --version $VERSION \
          --values argo-cd-values.yaml --namespace argocd --wait --timeout 900s

   Replace ``$VERSION`` with the Helm chart version (**not** the Argo CD application version) that you want to install.

If all goes well, you can now view the UI at ``/argo-cd`` and confirm that everything still looks correct.

If the ``helm upgrade`` command returns an error like this:

    Error: rendered manifests contain a resource that already
    exists. Unable to continue with install: Service
    "argocd-application-controller" in namespace "argocd" exists and
    cannot be imported into the current release: invalid ownership
    metadata; label validation error: key "app.kubernetes.io/managed-by"
    must equal "Helm": current value is "Tiller"; annotation validation
    error: missing key "meta.helm.sh/release-name": must be set to
    "argocd"; annotation validation error: missing key
    "meta.helm.sh/release-namespace": must be set to "argocd"

that means Argo CD was originally installed with Helm v2 and you're using Helm v3.
You can proceed with Helm v3, but you will need to fix all of the annotations and labels first.
For all namespaced resources, you can do this by running the following two commands for each resource type that ``helm upgrade`` warns about.

.. code-block:: console

   $ kubectl -n argocd label --overwrite $RESOURCE \
       -l "app.kubernetes.io/managed-by=Tiller" \
       "app.kubernetes.io/managed-by=Helm"
   $ kubectl -n argocd annotate $RESOURCE \
       -l "app.kubernetes.io/managed-by=Helm" \
       meta.helm.sh/release-name=argocd meta.helm.sh/release-namespace=argocd

Replace ``$RESOURCE`` with the type of the resource.
You should not use this command for non-namespaced resources (specifically ``ClusterRole`` and ``ClusterRoleBinding``).
For those resources, instead of using the ``-l`` selector, find the resources that are part of Argo CD via the ``argocd-`` prefix and then run the ``label`` and ``annotate`` commands naming them explicitly.
If you fix those non-namespaced resources and then iterate for each namespaced resource, eventually the ``helm upgrade`` command will succeed.

You should only have to do this once per cluster, and then subsequent upgrades with Helm v3 should work smoothly.

Recovering from a botched upgrade
=================================

If everything goes horribly wrong, you can remove Argo CD entirely and the restore it from the backup that you took.
To do this, first drop the Argo CD namespace:

.. code-block:: console

   $ kubectl delete namespace argocd

You will then need to manually remove the finalizers for all the Argo CD application resources in order for the namespace deletion to succeed.
The following instructions are taken from `an old Kubernetes issue <https://github.com/kubernetes/kubernetes/issues/77086>`__.

.. code-block:: console

   $ kubectl api-resources --verbs=list --namespaced -o name \
       | xargs -n 1 kubectl get --show-kind --ignore-not-found -n argocd

This will show all resources that need manual attention.
It should only be Argo CD ``Application`` and ``AppProject`` resources.
For each resource, edit it with ``kubectl edit -n argocd`` and delete the finalizer.
As you save each resource, its deletion should succeed.
By the end, the namespace should successfully finish deletion.
You can then recreate the namespace, reinstall Argo CD, and restore the backup.

.. code-block:: console

   $ kubectl create namespace argocd
   $ cd phalanx/installer
   $ helm upgrade --install argocd argo/argo-cd --version $HELM_VERSION \
       --values argo-cd-values.yaml --namespace argocd --wait --timeout 900s
   $ chmod 644 ~/.kube/config
   $ docker run -i -v ~/.kube:/home/argocd/.kube --rm \
       argoproj/argocd:$VERSION argocd-util import -n argocd - < backup.yaml
   $ chmod 600 ~/.kube/config

Replace ``$HELM_VERSION`` with the version of the Helm chart you want to use and ``$VERSION`` with the corresponding Argo CD version (as shown via ``helm search repo``).

This should hopefully restore Argo CD to a working state.
If it doesn't, you'll need to reinstall it using the more extended process used by the cluster installer.
See `installer/install.sh <https://github.com/lsst-sqre/phalanx/blob/master/installer/install.sh>`__ for the commands to run.
