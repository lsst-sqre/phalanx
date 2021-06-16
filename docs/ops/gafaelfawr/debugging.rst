#########
Debugging
#########

If a user successfully authenticates through the Gafaelfawr ``/login`` route but then cannot access a service such as the Notebook or Portal Aspects, a good initial debugging step is to look at the contents of the user's token.
Have the user go to ``/auth/analyze``, which will provide a JSON dump of their authentication information.
This will include their secret token, so be aware that sharing the full contents of that page will allow someone else to impersonate that user.
The important information is in the ``token.data`` portion of the JSON document.
The key information to look at is the ``isMemberOf`` claim, which shows the groups of which Gafaelfawr thinks the user is a member, and the ``scope`` claim, which shows how those group memberships were translated into access scopes using the ``group_mappings`` configuration.
This is usually the best tool for uncovering problems with group mapping.

For other issues, looking at the pod logs for the ``gafaelfawr`` pod in the ``gafaelfawr`` namespace is the best next step.
(The actual pod name will have a random string appended to ``gafaelfawr``.
The pod of interest is the one that is not the Redis pod.)
``kubectl logs <pod> -n gafaelfawr --timestamp`` or the Argo CD pod logs screen will show you the messages from Gafaelfawr, including any errors.
The logs from Gafaelfawr are in JSON format.
