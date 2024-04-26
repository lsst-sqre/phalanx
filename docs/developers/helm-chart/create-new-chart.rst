.. _dev-chart-starters:

###################################
Create new Helm chart from template
###################################

Ensure that your local Phalanx development environment is set up following the instructions in :doc:`/about/local-environment-setup`.

Then, create the files for the new application, including the start of a Helm chart:

.. prompt:: bash

   phalanx application create <application>

Replace ``<application>`` with the name of your new application, which will double as the name of the Helm chart.
The application name must start with a lowercase letter and consist of lowercase letters, numbers, and hyphen (``-``).

By default, this will create a Helm chart for a FastAPI web service created from the `SQuaRE template <https://safir.lsst.io/user-guide/set-up-from-template.html>`__.
Use the ``--starter`` flag to specify a different Helm chart starter.
There are three options:

fastapi-safir
    Use this starter for FastAPI web services based on Safir, created from the "FastAPI application (Safir)" template.
    This is the default.

web-service
    Use this starter if the new Helm application is some other web service.

empty
    Use this starter for any other type of application.
    This will create an empty Helm chart, to which you can add resources or external charts.

You will be prompted for a short description of the application.
Keep it succinct, ideally just a few words, and do not add a period at the end.
The description must begin with a capital letter.

You will also be prompted for the Argo CD project to use for your application.
This must be chosen from the list of projects at :doc:`/applications/index`.
See the page for each project for a short description of what it should contain.

Next steps
==========

- Flesh out the basic metadata for the Helm chart: :doc:`chart-yaml`
- Write the Kubernetes resource templates: :doc:`templates`
- Define the customization parameters for the chart: :doc:`values-yaml`
- Define the secrets for your application: :doc:`define-secrets`
