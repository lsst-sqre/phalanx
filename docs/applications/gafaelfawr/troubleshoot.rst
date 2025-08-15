.. px-app-troubleshooting:: gafaelfawr

###############
Troubleshooting
###############

.. _gafaelfawr-no-access:

User has no access to services
==============================

If a user successfully authenticates through the Gafaelfawr ``/login`` route but then cannot access an application such as the Notebook or Portal, or if Gafaelfawr tells them that they are not a member of any authorized groups, the problem is likely the user's group memberships.

GitHub
------

If the environment is using GitHub, there is no simple way to see Gafaelfawr's view of their group memberships other than finding the log message for their failed login.
However, one thing to check is if the organizational membership is private and the user didn't release it.
See :doc:`github-organizations` for more details about that problem.

If not, check that the user is indeed a member of the organizations and teams that should be granted access.
Sometimes the user forgot to accept the invitation to the group or team.

LDAP
----

For environments using LDAP, you can see the user's group information directly as an environment administrator.

As someone with ``admin:userinfo`` scope, go to :samp:`/auth/api/v1/users/{username}` in the corresponding Phalanx environment.
This will display the user's metadata from LDAP.
The important information is in the ``groups`` portion of the JSON document.
This shows the group membership as seen by Gafaelfawr.

Scopes are then assigned based on the ``config.groupMapping`` configuration in the ``values-*.yaml`` file for that environment.
Chances are good that the user is not a member of a group that conveys the appropriate scopes.

From there, the next step is usually to determine why the user is not a member of the appropriate group.

COmanage enrollment fails after prompting for attributes
========================================================

If all attempts to enroll new users in COmanage fail after the user enters their name and email address with the error "Please recheck the highlighted fields," the issue is probably with the enrollment attribute configuration.
If there is a problem with the configuration of a hidden field, the error message may be very confusing and non-specific.

Double-check the configuration of the "Self Signup With Approval" enrollment flow against :sqr:`055`.
Pay careful attention to the enrollment attributes, particularly the "Users group" configuration, which has a hidden value.
There is currently a bug in COmanage that causes it to not display the default values for attributes properly, so you may need to edit the enrollment attribute and set the default value again to be certain it's correct.

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
