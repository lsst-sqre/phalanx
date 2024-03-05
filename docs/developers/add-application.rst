################################
Add a new application to Phalanx
################################

This page provides the steps for integrating an application with Phalanx by adding the application's Helm chart.
This is the last step of adding a new application to Phalanx and should be done after you have :doc:`written the Helm chart <write-a-helm-chart>` and :doc:`defined the secrets it needs <define-secrets>`.

Some of the integration will be done for you by the :command:`phalanx application create` command, but you will need to make a few adjustments.

For background on building an application, see the :ref:`dev-build-toc` documentation.

.. warning::

   Although Phalanx uses Argo CD to manage applications, do not use the Argo CD command-line client to add new applications to a Phalanx environment.
   All Phalanx applications are managed inside Git and created through the Phalanx tooling.
   Applications created by the Argo CD command-line client will not be properly managed by Phalanx.

Add documentation
=================

Every new application added to Phalanx must have a corresponding folder in the `docs/applications directory <https://github.com/lsst-sqre/phalanx/tree/main/docs/applications>`__ containing at least an :file:`index.rst` file and a :file:`values.md` file.

Basic versions of these files were created by the :command:`phalanx application create` command (see :ref:`dev-chart-starters`).
However, you will need to edit :file:`index.rst` to add a longer description of the application at the top.
This should explain the purpose of the application and which environments should consider deploying it.

The :file:`values.md` file generally does not need to be modified.

Finally, add the new application to `docs/applications/index.rst <https://github.com/lsst-sqre/phalanx/blob/main/docs/applications/index.rst>`__ in the appropriate section.
Please maintain the alphabetical sorting of each section.

Configure other Phalanx applications
====================================

If the application needs to listen on hostnames other than the normal cluster-wide hostname, you will need to configure :px-app:`cert-manager` so that it can generate a TLS certificate for that hostname.
See :doc:`/applications/cert-manager/add-new-hostname` for more details.

If your application exposes Prometheus endpoints, you will want to configure these in the `telegraf application's prometheus_config <https://github.com/lsst-sqre/phalanx/blob/main/applications/telegraf/values.yaml>`__.

Enable the application for some environment
===========================================

Finally, you need to tell Argo CD to deploy your application in some environments.

#. For each environment in which your application will run, create a :file:`values-{environment}.yaml` file in your application's directory.
   This should hold only the customization specific to that Rubin Science Platform environment.
   Any shared configuration should go into the defaults of your chart (:file:`values.yaml`).

   If there is no environment-specific configuration, you must still create this file.
   In this case, leave it empty.

#. Enable your application in one of the :file:`values-{environment}.yaml` files in `environments <https://github.com/lsst-sqre/phalanx/tree/main/environments/>`__.
   Do this by adding a key for your application under ``applications`` (in alphabetical order) with a value of ``true``.
   This environment will be the first place your application is deployed.

   You almost certainly want to start in a development or integration environment and enable your new application in production environments only after it has been smoke-tested in less critical environments.

Next steps
==========

- Deploy your new application by switching a development environment to a branch: :doc:`switch-environment-to-branch`
- Test your application by deploying it from a branch: :doc:`deploy-from-a-branch`
