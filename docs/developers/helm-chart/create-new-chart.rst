.. _dev-chart-starters:

###################################
Create new Helm chart from template
###################################

Ensure that your local Phalanx development environment is set up following the instructions in :doc:`/about/local-environment-setup`.

Then, create the files for the new application, including the start of a Helm chart:

.. prompt:: bash

   phalanx application create <application> --project <project>

Replace ``<application>`` with the name of your new application, which will double as the name of the Helm chart.
The application name must start with a lowercase letter and consist of lowercase letters, numbers, and hyphen (``-``).

Replace ``<project>`` with the all-lowercase name of the Argo CD project that should contain the application.
This must be chosen from the list of projects shown at :doc:`/applications/index`.

By default, this will create a Helm chart for a FastAPI web service.
Use the ``--starter`` flag to specify a different Helm chart starter.
There are two options:

web-service
    Use this starter if the new Helm application is a web service, such as a new Safir_ FastAPI_ service.
    This is the default.

empty
    Use this starter for any other type of application.
    This will create an empty Helm chart, to which you can add resources or external charts.

You will be prompted for a short description of the application.
Keep it succinct, ideally just a few words, and do not add a period at the end.
The description must begin with a capital letter.

Next steps
==========

- Flesh out the basic metadata for the Helm chart: :doc:`chart-yaml`
- Write the Kubernetes resource templates: :doc:`templates`
- Define the customization parameters for the chart: :doc:`values-yaml`
- Define the secrets for your application: :doc:`define-secrets`
