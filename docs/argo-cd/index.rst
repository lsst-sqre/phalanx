#######
Argo CD
#######

.. list-table::
   :widths: 10,40

   * - Type
     - Helm_
   * - Namespace
     - ``argocd``

.. rubric:: Overview

`Argo CD`_ is the software that manages all Kubernetes resources in a deployment of the Rubin Science Platform.
It is itself a set of Kubernetes resources and running pods managed with `Helm`_.
Argo CD cannot manage and upgrade itself, so it periodically should be upgraded manually.

Argo CD is installed and bootstrapped as part of the cluster creation process.
The UI is exposed on the ``/argo-cd`` route for the Science Platform.
Unlike other resources on the Science Platform, it is not protected by Gafaelfawr.
It instead uses username and password authentication.
The username and password are stored in the SQuaRE 1Password vault.

.. rubric:: Warnings

Argo CD is somewhat particular about how its resources are set up.
Everything related to Argo CD that can be namespaced must be in the ``argocd`` namespace.

.. warning::

   ``Application`` resources must be in the ``argocd`` namespace, not in the namespace of the application.

If you accidentally create an ``Application`` resource outside of the ``argocd`` namespace, Argo CD will display it in the UI but will not be able to sync it.
You also won't be able to easily delete it if it defines the normal Argo CD finalizer because that finalizer will not run outside the ``argocd`` namespace.
To delete the stray ``Application`` resource, edit it with ``kubectl edit`` and delete the finalizer, and then delete it with ``kubectl delete``.

.. warning::

   Do not use the documented Argo CD upgrade method that uses ``kubectl apply``.
   This will not work properly when Argo CD was installed via Helm, as it is on the Science Platform, and it will create a huge mess.

Instead, follow the upgrade process described below.

.. rubric:: Guides

.. toctree::

   upgrading
   authentication
