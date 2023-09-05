.. px-app-notes:: argocd

##############################
Argo CD architecture and notes
##############################

Argo CD is installed and bootstrapped as part of the cluster creation process.
The UI is exposed on the ``/argo-cd`` route for the Science Platform.

Unlike other resources on the Science Platform, it is not protected by Gafaelfawr.
See :doc:`authentication`

Namespace for Application resources
===================================

Everything related to Argo CD that can be namespaced must be in the ``argocd`` namespace.

.. warning::

   ``Application`` resources must be in the ``argocd`` namespace, not in the namespace of the application.

   If you accidentally create an ``Application`` resource outside of the ``argocd`` namespace, Argo CD will display it in the UI but will not be able to sync it.
   You also won't be able to easily delete it if it defines the normal Argo CD finalizer because that finalizer will not run outside the ``argocd`` namespace.
   To delete the stray ``Application`` resource, edit it with ``kubectl edit`` and delete the finalizer, and then delete it with ``kubectl delete``.
