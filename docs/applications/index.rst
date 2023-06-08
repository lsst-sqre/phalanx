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
   datalinker/index
   hips/index
   linters/index
   livetap/index
   mobu/index
   moneypenny/index
   noteburst/index
   nublado/index
   nublado2/index
   portal/index
   semaphore/index
   sherlock/index
   sqlproxy-cross-project/index
   squareone/index
   ssotap/index
   tap/index
   tap-schema/index
   times-square/index
   vo-cutouts/index

.. toctree::
   :maxdepth: 1
   :caption: RSP+

   argo-workflows/index
   alert-stream-broker/index
   exposurelog/index
   narrativelog/index
   obsloctap/index
   plot-navigator/index
   production-tools/index
   sasquatch/index
   strimzi/index
   strimzi-access-operator/index
   strimzi-registry-operator/index
   telegraf/index
   telegraf-ds/index

.. toctree::
   :maxdepth: 1
   :caption: Roundtable

   kubernetes-replicator/index
   squarebot/index
