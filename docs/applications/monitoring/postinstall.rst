#######################
Post-Installation Setup
#######################

The monitoring application needs a little bit of manual configuration after installation.
While the admin token can be supplied from an existing secret, it is necessary to run ``tokenmaker`` to generate both the token that the tasks (which run as cronjobs) will require and the token that the ``telegraf`` and ``telegraf-ds`` scrapers will need in order to send their data to the monitoring database.

To do this:

* Clone the `rubin-influx-tools repository <https://github.com/lsst-sqre/rubin-influx-tools>`__ and change your current working directory to the clone location.
* Create a new virtualenv to work in.  Activate it.
* Run ``make init`` to install ``rubin-influx-tools`` into that virtualenv.
* Export the following environment variables:
   * ``INFLUXDB_ORG`` should be set to the influx organization, typically ``square``
   * ``INFLUXDB_TOKEN`` should be set to the admin token value, which can be found in 1Password.
   * ``INFLUXDB_URL`` should be set to the URL for the InfluxDBv2 server (e.g. ``https://monitoring.lsst.cloud``)
* Run ``tokenmaker`` and save the tokens, which will be logged to standard output.
* Clone `Phalanx <https://github.com/lsst-sqre/rubin-influx-tools>`__ and change to the clone location.
* Create another virtualenv, activate it, and run ``make init`` to install Phalanx.
* Export the following environment variables:
   * ``OP_CONNECT_TOKEN`` should be set to the correct 1Password Connect token for the Phalanx environment you're working on.  This can be found in 1Password.
   * ``VAULT_TOKEN`` should be set to the write token for the Phalanx environment you're working on.  This can also be found in 1Password.
   * ``VAULT_ADDR`` should be set to your Vault's URL, e.g. ``https://vault.lsst.cloud``
* In 1Password, find the set of secrets for the Phalanx environment you're working on.  Open the ``monitoring`` secret.  Edit the ``influx-alert-token`` password's value, and change it to the value of "Token for task/alert creation" that was displayed when you ran ``tokenmaker``.
* Run ``phalanx secrets audit <environment>``; this should show only the ``influx-alert-token`` with an unexpected value.  If anything else is incorrect, fix that first before coming back here.
* Run ``phalanx secrets sync <environment>``.  This will store the new token into Vault.
* Either wait 15 minutes, or delete the ``monitoring`` secret from the ``monitoring`` namespace in your Phalanx environment.  This will recreate the secret with the new (correct) value.

This should get the "monitoring" application going.

For ``telegraf`` and ``telegraf-ds`` (for each instance you want to repoint), it will be necessary to create a Phalanx branch, change ``config.influxdb2Url`` to the new server endpoint, and update their influx-token secrets to use the "Token for remote telegraf bucket writing" that ``tokenmaker`` created.  We can't just share the secret because the telegraf scrapers are very likely to be running in a completely different Kubernetes cluster and location than the database.
