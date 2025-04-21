.. px-app:: grafana

#####################################################
grafana — Observability visualization
#####################################################

.. warning::

   After the Grafana instance is provisioned, DO NOT CHANGE THE ADMIN PASSWORD without understanding and following :ref:`these instructions <changing-the-admin-password>`!

This app installs the `Grafana Operator`_ and a `Grafana`_ instance.
Other Phalanx applications can provision their own Grafana resources, like dashboards and alerts, in their own config by using the CRDS installed by the Grafana Operator.
These resources will be provisioned in the Grafana instance created by this application.

.. _Grafana: https://grafana.com
.. _Grafana Operator: https://grafana.github.io/grafana-operator/

.. jinja:: grafana
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   installation
   changing-the-admin-password
   operator-usage
   upgrading
   disaster-recovery
   values
