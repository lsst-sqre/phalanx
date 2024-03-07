############
Pull secrets
############

If your application image resides at a Docker repository which requires authentication (either to pull the image at all or to raise the pull rate limit), then you must tell any pods deployed by your application to use a pull secret named ``pull-secret``, and you must create a ``VaultSecret`` resource for that pull secret.

.. note::

   If your container image is built through GitHub Actions and stored at ghcr.io (the recommended approach), there is no rate limiting (as long as your container image is built from a public repository, which it should be).
   There is therefore no need for a pull secret and you can skip the rest of this section.

If your container image is stored at Docker Hub, you should use a pull secret, because we have been (and will no doubt continue to be) rate-limited at Docker Hub.
Strongly consider moving your container image to the GitHub Container Registry (ghcr.io) instead.

If your container image is pulled from a private repository, you may need authentication and therefore a pull secret.

Add the pull secret to pods
===========================

If you do need a pull secret, add a block like the following to the pod specification for any resource that creates pods.

.. code-block:: yaml
   :caption: deployment.yaml

   imagePullSecrets:
     - name: "pull-secret"

If you are using an external chart, see its documentation for how to configure pull secrets.

Add the pull-secret Kubernetes resource
=======================================

Then, add the following ``VaultSecret`` to your application templates to put a copy of ``pull-secret`` in your application's namespace:

.. code-block:: yaml
   :caption: vault-secrets.yaml

   apiVersion: ricoberger.de/v1alpha1
   kind: VaultSecret
   metadata:
     name: pull-secret
     labels:
       {{- include "<application>.labels" . | nindent 4 }}
   spec:
     path: "{{- .Values.global.vaultSecretsPath }}/pull-secret"
     type: kubernetes.io/dockerconfigjson

Replace ``<application>`` with the name of your application.
If you already have another ``VaultSecret`` resource, put a line containing only ``---`` between them.
(This is the standard YAML syntax for putting mutiple objects in the same file.)

The pull secret itself is managed globally for the environment, usually by the environment administrator.
See :doc:`/admin/update-pull-secret` for details on how to modify the pul secret if necessary.
