############
Applications
############

Applications are individual *atomic* services that are configured and deployed through Phalanx.
Each environment can opt whether to deploy an application, and also customize the configuration of the application.
This section of the documentation describes each Phalanx application.

The category names correspond to the project name in phalanx/applications/_project_.
Infrastructure is specifically reserved for applications that are necessary for "proof of life" deployments, eg by non-Rubin deployers who are only interested in phalanx as an internal developer environment.

To learn how to develop applications for Phalanx, see the :doc:`/developers/index` section.

.. toctree::
   :maxdepth: 1
   :caption: infrastructure ("bare" Phalanx infrastructure)

   argocd/index
   cert-manager/index
   ingress-nginx/index
   gafaelfawr/index
   mobu/index
   postgres/index
   strimzi/index
   strimzi-access-operator/index
   vault-secrets-operator/index

.. toctree::
   :maxdepth: 1
   :caption: rsp (Rubin Science Platform)

   butler/index
   datalinker/index
   filestore-backup/index
   hips/index
   jira-data-proxy/index
   livetap/index
   noteburst/index
   nublado/index
   portal/index
   semaphore/index
   siav2/index
   sqlproxy-cross-project/index
   squareone/index
   ssotap/index
   tap/index
   times-square/index
   vo-cutouts/index

.. toctree::
   :maxdepth: 1
   :caption: rubin: Additional Rubin services

   alert-stream-broker/index
   exposurelog/index
   narrativelog/index
   obsloctap/index
   plot-navigator/index
   production-tools/index
   rubintv/index
   schedview-prenight/index
   schedview-snapshot/index

.. toctree::
   :maxdepth: 1
   :caption: roundtable Roundtable

   giftless/index
   kubernetes-replicator/index
   monitoring/index
   onepassword-connect/index
   ook/index
   squarebot/index

.. toctree::
   :maxdepth: 1
   :caption: monitoring (Monitoring and metrics)

   linters/index
   sasquatch/index
   sherlock/index
   telegraf/index
   telegraf-ds/index

.. toctree::
   :maxdepth: 1
   :caption: prompt (Prompt Processing)

   next-visit-fan-out/index
   prompt-proto-service-hsc/index
   prompt-proto-service-latiss/index
   prompt-proto-service-lsstcam/index
   prompt-proto-service-lsstcomcam/index

.. toctree::
   :maxdepth: 1
   :caption: telescope (Rubin Observatory Control System and related services)

   argo-workflows/index
   auxtel/index
   calsys/index
   control-system-test/index
   eas/index
   love/index
   obssys/index
   simonyitel/index
   uws/index
