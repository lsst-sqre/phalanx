##################
Checking the chart
##################

Most of the testing of your chart will have to be done by deploying it in a test Kubernetes environment.
See :doc:`add-application` for more details about how to do that.
However, you can check the chart for basic syntax and some errors in Helm templating before deploying it.

To check your chart, run:

.. prompt:: bash

   phalanx application lint <application>

Replace ``<application>`` with the name of your new application.
Multiple applications may be listed to lint all of them.

This will run :command:`helm lint` on the chart with the appropriate values files and injected settings for each environment for which it has a configuration and report any errors.
:command:`helm lint` does not check resources against their schemas, alas, but it will at least diagnose YAML and Helm templating syntax errors.

You can limit the linting to a specific environment by specifying an environment with the ``--environment`` (or ``-e`` or ``--env``) flag.

This lint check will also be done via GitHub Actions when you create a Phalanx PR, and the PR cannot be merged until this lint check passes.

You can also ask for the fully-expanded Kubernetes resources that would be installed in the cluster when the chart is installed.
Do this with:

.. prompt:: bash

   phalanx application template <application> <environment>

Replace ``<application>`` with the name of your application and ``<environment>`` with the name of the environment for which you want to generate its resources.
This will print to standard output the expanded YAML Kubernetes resources that would be created in the cluster by this chart.
