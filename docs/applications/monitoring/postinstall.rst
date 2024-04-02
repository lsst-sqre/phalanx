#######################
Post-Installation Setup
#######################

The monitoring application requires substantial manual configuration after installation.

Secrets And Tokens
==================

While the admin token can be supplied from an existing secret, it is
necessary to run ``tokenmaker`` to generate the token that the tasks
(which run as cronjobs) will require and the token that the ``telegraf`` and ``telegraf-ds`` scrapers will need in order to send their data to the monitoring database.

Set up the Environment
----------------------

* Clone the `rubin-influx-tools repository <https://github.com/lsst-sqre/rubin-influx-tools>`__ and change your current working directory to the clone location.
* Create a new virtualenv to work in.  Activate it.
* Run ``make init`` to install ``rubin-influx-tools`` into that virtualenv.
* Export the following environment variables:

   * ``INFLUXDB_ORG`` should be set to the influx organization, typically ``square``
   * ``INFLUXDB_TOKEN`` should be set to the admin token value, which can be found in 1Password under the ``admin-token`` entry.
   * ``INFLUXDB_URL`` should be set to the URL for the InfluxDBv2 server (e.g. ``https://monitoring.lsst.cloud``)
* Run ``tokenmaker``.  You will need the two tokens created.  If you are not using 1Password, save them somewhere safe.  If you are:

   * In 1Password, find the set of secrets for the Phalanx environment you're working on.
   * Open the ``monitoring`` secret.
   * Edit the ``influx-alert-token`` password's value, and change it to the value of "Token for task/alert creation" that was displayed when you ran ``tokenmaker``.
   * Edit the ``telegraf-token`` password's value, and change it to the value of "Token for remote telegraf bucket writing" that was displayed when you ran ``tokenmaker``.
   * Save the secret.
* Audit the secrets: :doc:`/admin/audit-secrets`.  This should show only ``influx-alert-token`` and ``telegraf-token`` with unexpected values in the ``monitoring`` app.  If anything else is incorrect, fix that first before coming back here.
* Sync the secrets: :doc:`/admin/sync-secrets`.
* Delete the ``monitoring`` secret from the ``monitoring`` namespace in your Phalanx environment.  It will be recreated with the new values.  This step is not necessary, but you may have to wait up to 15 minutes for the secret to be updated.

This should suffice to get the "monitoring" application going.

Chronograf
==========

Now it is very important that you be the first person to visit the Chronograf endpoint and authenticate (it will use the local Gafaelfawr instance to do so).


Initial Chronograf Configuration
--------------------------------

It will be at the ``/chronograf`` path on the general Phalanx instance endpoint.

Log in with OIDC.

This will create your user and make you a super-admin.

You will see a screen with a ``Get Started`` button, which you should press.

To set up the connection to influxDBv2:

* Switch the auth method to "InfluxDB v2 Auth" at the bottom left.
* Set ``Connection URL`` to the InfluxDB endpoint (e.g. ``https://monitoring.lsst.cloud``).
* Set ``Organization`` to the InfluxDB org, usually ``square``.
* Paste the admin token into the ``Token`` field.
* Set the default retention policy.  ``30d`` is typical, and if you don't have a strong opinion, use it.
* Press the "Add Connection" button.

Next, skip dashboard creation (``Skip`` at the bottom center of the screen).

Skip Kapacitor setup as well on the next screen.  Press ``View All Connections``.

Now you should be at the Chronograf main UI screen.

Chronograf User Policy
----------------------

By clicking the crown icon (``Admin``) on the left side of the screen, and then choosing ``Chronograf``, and then the "All Users" tab, you can decide whether new users should be super-admins by default or not.
Since there is no mapping from Gafaelfawr scope to Chronograf abilities, you almost certainly do not them to be, and you will have to give new users admin powers (if they should have them) when they first log in.
After there are more admins, of course, someone else can empower new users as they come onboard.

Load dashboards
---------------

Finally, load the Chronograf dashboards from https://github.com/lsst-sqre/rubin-influx-tools/tree/main/src/rubin_influx_tools/dashboards/chronograf, using the ``Import Dashboard`` button in the upper left of the ``Dashboards`` screen, acessible through the ``Dashboard`` (bunch-of-rectangles) icon on the left side of the main screen.

For each dashboard, take the default options for "Sources in Dashboard".


Monitoring Agents
=================

You will need to update the ``influx-token`` secret in any environment that is feeding your new monitoring server, so that the telegraf and telegraf-ds agents are able to talk to it.
This is why it was convenient to save ``telegraf-token`` in the 1Password vault for the ``monitoring`` server's environment, because you can trivially cut-and-paste it.
Sync the secrets: :doc:`/admin/sync-secrets` and delete the ``telegraf`` and ``telegraf-ds`` secrets in their respective namespaces if you're impatient.
After the secrets are synced, restart the agents; for ``telegraf`` that's the deployment, and for ``telegraf-ds`` it's the daemonset.
