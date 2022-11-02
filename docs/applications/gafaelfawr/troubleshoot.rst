.. px-app-troubleshooting:: gafaelfawr

###############
Troubleshooting
###############

User has no access to services
==============================

If a user successfully authenticates through the Gafaelfawr ``/login`` route but then cannot access an application such as the Notebook or Portal, or if Gafaelfawr tells them that they are not a member of any authorized groups, start by determining what groups the user is a member of.

Have the user go to ``/auth/api/v1/user-info``, which will provide a JSON dump of their authentication information.
There is nothing secret in this information, so they can safely cut and paste it into a help ticket, Slack, etc.

The important information is in the ``groups`` portion of the JSON document.
This shows the group membership as seen by Gafaelfawr.
Scopes are then assigned based on the ``config.groupMapping`` configuration in the ``values-*.yaml`` file for that environment.
Chances are good that the user is not a member of a group that conveys the appropriate scopes.

From there, the next step is usually to determine why the user is not a member of the appropriate group.
Usually this means they weren't added or (in the case of groups from GitHub teams) didn't accept the invitation.

For a new GitHub configuration, it's possible that the organizational membership is private and the user didn't release it.
See :doc:`github-organizations` for more details about that problem.

Viewing logs
============

For other issues, looking at the pod logs for the ``gafaelfawr`` deployment in the ``gafaelfawr`` namespace is the best next step.
The best way to look at current logs is via Argo CD, which will group together the logs from all pods managed by that deployment and optionally add timestamps.

Find the ``Deployment`` resource named ``gafaelfawr`` (not the Redis or tokens deployment) and choose :guilabel:`Logs` from the menu.
Then, use the :guilabel:`Containers` button (it looks like three horizontal lines with the middle one offset) at the top and select the ``gafaelfawr`` container.
That will show a merged view of the logs of all of the pods, and you can look for error messages.

You can also add timestamps to the start of each line and download the logs with other buttons at the top.
Downloading logs will give you somewhat older logs, although usually only about a half-hour's worth since Gafaelfawr generates a lot of logs.

The logs from Gafaelfawr are in JSON format.
The best way to search older logs (and arguably the best way to look at current logs) is to use a JSON-aware log view and search tool if available for the environment that you're debugging.
For the IDF environments, use `Google Log Explorer <https://cloud.google.com/logging/docs/view/logs-explorer-interface>`__.
