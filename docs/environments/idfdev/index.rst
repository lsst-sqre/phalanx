##########################
idfdev: idf-dev.lsst.cloud
##########################

idfdev is a development environment for the Rubin Science Platform at the IDF (hosted on Google Cloud Platform).
The primary use of idfdev is for application development by the SQuaRE team.

.. list-table::

   * - Phalanx name
     - ``idfdev``
   * - Root domain
     - `data-dev.lsst.cloud <https://data-dev.lsst.cloud>`__
   * - Identity provider
     - ``ldaps://ldap-test.cilogon.org``
   * - Gafaelfawr groups
     - .. list-table::

          * - Role
            - Groups
          * - ``admin:provision``
            - - ``g_science-platform-idf-dev``
          * - ``exec:admin``
            - - ``g_science-platform-idf-dev``
          * - ``exec:notebook``
            - - ``g_science-platform-idf-dev``
          * - ``exec:portal``
            - - ``g_science-platform-idf-dev``
          * - ``read:image``
            - - ``g_science-platform-idf-dev``
          * - ``read:tap``
            - - ``g_science-platform-idf-dev``
   * - Argo CD
     - https://data-dev.lsst.cloud/argo-cd
   * - Argo CD access
     - .. code-block:: text

          g, adam@lsst.cloud, role:admin
          g, afausti@lsst.cloud, role:admin
          g, christine@lsst.cloud, role:admin
          g, dspeck@lsst.cloud, role:admin
          g, frossie@lsst.cloud, role:admin
          g, jsick@lsst.cloud, role:admin
          g, krughoff@lsst.cloud, role:admin
          g, rra@lsst.cloud, role:admin
          g, gpdf@lsst.cloud, role:admin
          g, loi@lsst.cloud, role:admin
          g, roby@lsst.cloud, role:admin

   * - Applications
     - - `argocd <#>`__ — `values-idfdev.yaml <#>`__ + `values.yaml <#>`__
       - `gafaelfawr <#>`__ — `values-idfdev.yaml <#>`__ + `values.yaml <#>`__
