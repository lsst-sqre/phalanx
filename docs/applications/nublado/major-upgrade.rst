###############################
Nublado major version migration
###############################

Currently we only discuss nublado v2 to nublado v3 migration; when the
next major version comes about, we'll add those instructions as well.

In general, when a new version appears, it will be called ``nublado``
and the previous version will be ``nubladoN`` where N is currently 2,
and will be 3 when we do another major version (that is, the
just-superseded version will be renamed on release of the newly-current
one).

Nublado 2 to Nublado 3 Migration
================================

Upgrading nublado v2 to nublado v3 is a complex process, and is usually
done in stages; in the general case, each of these three stages would
take place in a separate maintenance window as defined by site policy:

#. Enable nublado v3 on a non-default route (i.e. not ``/nb``; in this
   document and in actuality, we use ``/n3``).  Run for some time
   allowing users to test the new spawner while still using nublado v2
   by default
#. Switch nublado v3 to ``/nb`` and nublado v2 to an alternate route
   (e.g. ``/n2``).  Again, run for some time, keeping an eye out for any
   problems.
#. Once satisfied with the performance of nublado v3, disable the
   ``nublado2``, ``cachemachine``, and ``moneypenny`` applications (the
   functionality of the latter two are subsumed in nublado v3).
#. Once every environment is migrated, delete the ``nublado2``,
   ``cachemachine``, and ``moneypenny`` applications from Phalanx.

Enable nublado v3
-----------------

Pre-deployment Preparation
^^^^^^^^^^^^^^^^^^^^^^^^^^

The following tasks can be performed at any time, and should be
performed ahead of your maintenance window to actually turn on the
application.

Vault Secret Creation
"""""""""""""""""""""

The first thing you will need to do is to set up secrets for
``nublado`` (in future versions, this will require copying ``nublado``
to ``nubladoN``, but ``nublado2`` is the current name for version 2, so
if you're running an RSP, you already have those secrets set up
correctly).

These secrets, stored in Vault, and presented by
``vault-secrets-operator`` are:

#. ``cryptkeeper_key``: may be randomly generated; used internally by
   the Hub to encrypt authentication state in the session database.
#. ``crypto_key``: may be randomly generated; used to encrypt cookies
   for user state in the browser session.
#. ``proxy_token``: may be randomly generated; used to encrypt
   communications between the JupyterHub Configurable HTTP Proxy and the
   Hub.
#. ``hub_db_password``: the password for the Hub session database; in
   nublado v3 this is a Postgres database; conventionally both the
   username and the database name are ``nublado3``.  In general you
   should be consuming a database as a service, in which case you will
   need to request this database from your DBAs and ask them the
   password.  If you are instead running the internal database, you will
   need to create this database and grant permissions in the
   ``postgres`` application configuration.
#. ``slack_webhook``: the Slack webhook allowing the JupyterLab
   controller to post status messages to Slack.  This is the same one as
   used by, e.g. Gafaelfawr in your RSP instance.

Note that in future the secret setup and management will all be handled
as part of Phalanx deployment, and you will no longer need to do this
manually.  However, at the present, you still do.

Enable the application
""""""""""""""""""""""

In the values file for your installation in the top-level Phalanx
``environments`` directory, set ``nublado: true``.

Configure nublado v3
""""""""""""""""""""

In the values file for your installation in ``applications/nublado``,
set up your site-specific values.  The bulk of this work will be
specifying the set of mount points you use for persistent user data.
More than likely, you will use the same mount points for nublado v3 as
you did for nublado v2, but the configuration syntax differs.

Note that if you do share persistent storage between nublado versions,
the step about communicating with your users (below) goes from
"important" to "critical".

Create an alternate route
"""""""""""""""""""""""""

In the values file for your installation in ``applications/nublado``,
set the key ``jupyterhub.hub.baseUrl`` to ``/n3``.

Communicate to user base
""""""""""""""""""""""""

Let your users know about the new route and when it will be enabled
(presumably, at the end of the next maintenance window).  Announce that
that maintenance window will be disruptive and will destroy any existing
user sessions.

If you are using the same storage for users regardless of which spawner
they're coming in as, which you very likely are, in addition to the new
route, you need to do your utmost to make it extremely clear that if
they are testing the new route, it is vital to make sure that their labs
from the previous route are shut down before changing from one route to
the other.  If they do not do this, it will at best create confusion as
open notebooks will be saved every five minutes by each environment,
thus bafflingly reverting changes, and at worst it will cause full-scale
corruption of the files the user has open.


Silence Mobu complaints
"""""""""""""""""""""""

Turn off ``mobu`` for notebooks if you're using it, so that it doesn't
complain about the service outage.  The easiest way to do this is, as an
administrator, is to issue an HTTP ``DELETE`` against
``/mobu/flocks/<flockname>``.  Note that none of the silencing/disabling
steps require any changes to Phalanx; they are all being performed in
the ArgoCD UI or the Kubernetes CLI, and will be undone by a sync at the
end of the maintenance window.

Disable logins
""""""""""""""

Disable user logins to nublado v2.  This is most easily done by deleting
the ``hub`` deployment from nublado v2.

Remove user sessions
""""""""""""""""""""

Remove any user sessions.  You can do this by deleting the namespace
objects in the ``nublado-users`` application (which will also clean up
anything within those namespaces) or by executing something like
``kubectl get ns | grep nublado2- | awk '{print $1}' | xargs kubectl
delete ns``.

Bring up applications
"""""""""""""""""""""
#. Synchronize the ``science-platform`` application.  This will enable
   the ``nublado`` application, which contains nublado v3.
#. Synchronize the ``nublado`` application.  This will turn on the
   nublado v3 spawner.
#. Test that you can get a lab and that that lab allows use of the
   command line and cell executions with the new spawner at ``/n3``.  If
   you find errors, troubleshoot them.  Only proceed once you have the
   new spawner correctly spawning and shutting down labs.
#. Synchronize the ``nublado2`` application.  This will reenable the
   default spawner at ``/nb``.  At this point users will start returning
   (whether or not you call an all-clear, which you should not yet;
   users don't pay attention to such things).
#. Re-enable mobu, if you disabled any of its flocks, by syncing the
   ``mobu`` application.  Wait to make sure it's correctly running
   notebooks, or test a few yourself.

Make nublado v3 the default
---------------------------

Pre-deployment Preparation
^^^^^^^^^^^^^^^^^^^^^^^^^^
As before, these steps can be done at any time, and should be done in
advance of the maintenance window.

Communicate to user base
""""""""""""""""""""""""

Let your users know that ``/nb`` will refer to the new spawner, and that
the old one will be available for a while at ``/n2``, as well as the
timeframe for these changes (presumably, at the end of the next
maintenance window).  Announce that that maintenance window will be
disruptive and will destroy any existing user sessions.

If you are using the same storage for users regardless of which spawner
they're coming in as, which you very likely are, in addition to the new
route, you need to do your utmost to make it extremely clear that if
they intend to use both routes, it is vital to make sure that their labs
from the previous route are shut down before changing from one route to
the other.  If they do not do this, it will at best create confusion as
open notebooks will be saved every five minutes by each environment,
thus bafflingly reverting changes, and at worst it will cause full-scale
corruption of the files the user has open.

Change mobu configuration
"""""""""""""""""""""""""

If you are using ``mobu``, change the instance-specific values file.  In
``config.autostart``, for each entry, set ``business.use_cachemachine`` to
``false``.  This is necessary because nublado 3 uses its Jupyterlab
Controller to carry out the functions formerly performed by
``cachemachine``.

Change nublado2 configuration
"""""""""""""""""""""""""""""

In the values file for your installation in ``applications/nublado2``,
set the key ``jupyterhub.hub.baseUrl`` to ``/n2``.

Change nublado3 configuration
"""""""""""""""""""""""""""""

Remove the key ``jupyterhub.hub.baseUrl`` from the values file for your
installation in ``applications/nublado``.

This and the preceding step will make nublado v3 your default spawner on
the ``/nb`` route and will relegate nublado v2 to the ``/n2`` route

Deployment
^^^^^^^^^^

During the deployment window:

Silence Mobu complaints
"""""""""""""""""""""""

Turn off ``mobu`` for notebooks if you're using it, so that it doesn't
complain about the service outage.  The easiest way to do this is, as an
administrator, is to issue an HTTP ``DELETE`` against
``/mobu/flocks/<flockname>``.  Note that none of the silencing/disabling
steps require any changes to Phalanx; they are all being performed in
the ArgoCD UI or the Kubernetes CLI, and will be undone by a sync at the
end of the maintenance window.


Disable logins
""""""""""""""

Disable user logins to nublado v2 and nublado v3.  This is most easily
done by deleting the ``hub`` deployment from each of the ``nublado2``
and ``nublado`` applications.

Remove user sessions
""""""""""""""""""""

Remove any user sessions.  You can do this by deleting the namespace
objects in the ``nublado-users`` application (which will also clean up
anything within those namespaces) or by executing something like ``for i
in '' 2; do kubectl get ns | grep nublado${i}- | awk '{print $1}' |
xargs kubectl delete ns; done``.

Bring up applications
"""""""""""""""""""""
#. Synchronize the ``nublado2`` application.  This will move the
   default spawner to the ``/n2`` route.
#. Test that you can get a lab and that that lab allows use of the
   command line and cell executions with the new spawner at ``/n2``.  If
   you find errors, troubleshoot them.  If nublado v2 was working
   correctly beforehand, there should be no errors.
#. Synchronize the ``nublado`` application.  This will turn on the
   nublado v3 spawner on the default route ``/nb``.  At this point users
   will start returning (whether or not you call an all-clear, which you
   should not yet; users don't pay attention to such things).
#. Re-enable mobu, if you disabled it, by resynchronizing it from the
   ArgoCD UI.  Wait to make sure it's correctly running notebooks, or
   test a few yourself.

Disable nublado v2
------------------

Pre-deployment Preparation
^^^^^^^^^^^^^^^^^^^^^^^^^^
As before, these steps can be done at any time, and should be done in
advance of the maintenance window.

Communicate to user base
""""""""""""""""""""""""

Let your users know that ``/n2`` will no longer available.  Announce that
that maintenance window will be disruptive and will destroy any user
sessions spawned via ``/n2``.  Hopefully that will be none or at least
very few.

Turn off nublado v2
"""""""""""""""""""

Delete the entries ``cachemachine: true``, ``moneypenny: true``, and
``nublado2: true`` from your instance-specific values file in
``environment``.

Deployment
^^^^^^^^^^

During the deployment window:

#. Synchronize the ``science-platform`` application.  This will delete
   the ``nublado2``, ``cachemachine``, and ``moneypenny`` applications.
#. Remove any user sessions spawned by ``nublado2``.  This is harder to
   do from the UI: you will need to find any users in ``nublado-users``
   with a namespace called ``nublado2-<username>`` and remove only those
   namespaces.  From the CLI, it's easier: ``kubectl get ns | grep
   nublado2- | awk '{print $1}' | xargs kubectl delete ns``.
#. Delete the values files for your environment from Phalanx's
   ``applications/nublado2``, ``applications/cachemachine``, and
   ``applications/moneypenny``.

When Migration Is Complete For All Sites
-----------------------------------------

#. Once all sites are running nublado v3, and none are still running
   nublado v2, the directories ``applications/nublado2``,
   ``applications/moneypenny``, and ``applications/cachemachine`` can all
   be deleted from Phalanx.
#. Remove the ``nublado2`` secret from the vault enclave for all
   environments.
#. Remove the ``jupyterhub`` database and ``jovyan`` user from the
   postgres instance for each environment (or have the site DBA do it if
   it's a database you don't manage).
