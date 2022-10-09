############
Applications
############

Applications are individual *atomic* services that are configured and deployed through Phalanx.
Each environment can opt whether to deploy an application, and also customize the configuration of the application.
This section of the documentation describes each Phalanx application.

To learn how to develop applications for Phalanx, see the :doc:`/developers/index` section.

.. toctree::
   :maxdepth: 1
   :caption: Cluster infrastructure

   argo-cd/index
   cert-manager/index
   ingress-nginx/index
   gafaelfawr/index
   postgres/index
   vault-secrets-operator/index

.. toctree::
   :maxdepth: 1
   :caption: Rubin Science Platform

   cachemachine/index
   mobu/index
   nublado2/index
   tap/index
