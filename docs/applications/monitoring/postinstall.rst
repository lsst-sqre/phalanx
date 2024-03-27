#######################
Post-Installation Setup
#######################

The monitoring application requires substantial manual configuration after installation.

Secrets And Tokens
==================

While the admin token can be supplied from an existing secret, it is necessary to run ``tokenmaker`` to generate the token that the tasks (which run as cronjobs) will require, the token that the ``telegraf`` and ``telegraf-ds`` scrapers will need in order to send their data to the monitoring database.

You will also need the client secret for Chronograf to communicate with Gafaelfawr.  This will have been generated when you syncronized the secrets for ``monitoring``.

Set up the Environment
----------------------

* Clone the `rubin-influx-tools repository <https://github.com/lsst-sqre/rubin-influx-tools>`__ and change your current working directory to the clone location.
* Create a new virtualenv to work in.  Activate it.
* Run ``make init`` to install ``rubin-influx-tools`` into that virtualenv.
* Export the following environment variables:
   * ``INFLUXDB_ORG`` should be set to the influx organization, typically ``square``
   * ``INFLUXDB_TOKEN`` should be set to the admin token value, which can be found in 1Password under the ``admin-token`` entry.
   * ``INFLUXDB_URL`` should be set to the URL for the InfluxDBv2 server (e.g. ``https://monitoring.lsst.cloud``)
* Run ``tokenmaker`` and save the tokens, which will be logged to standard output (or just leave them onscreen while you do the next step).
* In 1Password, find the set of secrets for the Phalanx environment you're working on.  Open the ``monitoring`` secret.  Edit the ``influx-alert-token`` password's value, and change it to the value of "Token for task/alert creation" that was displayed when you ran ``tokenmaker``.  Edit the ``telegraf-token`` password's value, and change it to the value of "Token for remote telegraf bucket writing" that was displayed when you ran ``tokenmaker``.  Save the secret.
* Run ``phalanx secrets audit <environment>``; this should show only ``influx-alert-token`` and ``telegraf-token`` in the ``monitoring`` app, and ``influx-token`` in ``telegraf-ds``, with unexpected values.  If anything else is incorrect, fix that first before coming back here.
* Run ``phalanx secrets sync <environment>``.  This will store the new tokens into Vault.
* Delete the ``monitoring`` secret from the ``monitoring`` namespace in your Phalanx environment (and, if ``telegraf-ds`` is installed, the ``telegraf`` secret from the ``telegraf-ds`` namespace).  This will recreate the secret(s) with the new (correct) value.

This should suffice to get the "monitoring" application going.

Chronograf
==========

Now it is very important that you be the first person to visit the Chronograf endpoint and authenticate (it will use the local Gafaelfawr instance to do so).


Initial Chronograf Configuration
--------------------------------

It will be at the ``/chronograf`` path on either the ``monitoring`` endpoint or the general Phalanx instance endpoint.

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
