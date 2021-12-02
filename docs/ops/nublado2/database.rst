############################
Clear session database entry
############################

Sometimes JupyterHub and its session database will get into an inconsistent state where it thinks a pod is already running but cannot shut it down.
The typical symptom of this is that spawns for that user fail with an error saying that the user's lab is already pending spawn or pending deletion, but the user cannot connect to their pod.

Recovery may require manually clearing the user's entry in the session database as follows:

#. Remove the user's lab namespace, if it exists.
  
#. Remove the user from the session database.
   Connect to the database with:
  
   .. code-block:: shell

      pod=$(kubectl get pods -n postgres | grep postgres | awk '{print $1}')
      kubectl exec -it -n postgres ${pod} -- psql -U jovyan jupyterhub
	
   and then, at the PostgreSQL prompt, run:

   .. code-block:: sql

      delete from users where name='<user-to-remove>'

In some cases you may also need to remove the user from the spawner table.
To do this, run ``select * from spawners`` and find the pod with the user's name in it, and then delete that row.
