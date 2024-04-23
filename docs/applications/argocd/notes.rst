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

TLS configuration merging
=========================

This applies only to environments that use Let's Encrypt for certificate management.

Because all application ingresses share the same external hostname, the way the ingress configuration is structured in Phalanx is somewhat unusual.
Nearly all application create an ingress without adding TLS configuration.
Instead, they all use the same hostname, without a TLS stanza.
The Argo CD ingress is the one designated ingress with a TLS configuration to request creation of certificates.
Because each ingress uses the same hostname, :px-app:`ingress-nginx` will merge all of those ingresses into one virtual host and will set up TLS if TLS is defined on any of them.

Were TLS defined on more than one ingress, only one of those TLS configurations would be used, but which one is chosen is somewhat random.
Therefore, we designate Argo CD as the single application to hold the configuration to avoid any confusion from unused configurations.
