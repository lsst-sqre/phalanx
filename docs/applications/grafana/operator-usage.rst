##################
Using the Operator
##################

The `Grafana operator`_ installs CRDs to manage different kinds of Grafana configuration in your app's own Phalanx config.
The most useful are probably the ``GrafanaDashboard`` and ``GrafanaAlertRuleGroup`` CRDs.
Unfortunately, the specs for these are really nasty.
They are almost impossible to create by hand, and even hard to edit by hand.

The recommended process for creating one of these is to:

#. Create it manually in the Grafana UI.
#. Export it as JSON through the Grafana UI and save the JSON.
#. Delete it through the Grafna UI.
#. Use the exported JSON to create the resource in your app's Phalanx config using the exported JSON.

Once you have created a dashboard or alert through one of these CRDs, any changes you make to it through the Grafana UI will be revered to the version specified in the Phalanx config.
For simple changes, you can edit the resource in the Phalanx config directly.
For more complex changes, you can:

#. Make a copy of the thing manually in the Grafana UI.
#. Make your changes to the copy.
#. Export the copy as JSON and save the JSON.
#. Replace the JSON in the Phalanx config with the new JSON.
#. Delete the copy in the Grafana UI.


.. _Grafana operator: https://grafana.github.io/grafana-operator/
.. _GrafanaDashboard: https://grafana.github.io/grafana-operator/docs/dashboards/
.. _GrafanaAlertRuleGroup: https://grafana.github.io/grafana-operator/docs/alerting/alert-rule-groups/
