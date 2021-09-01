################
Database Surgery
################

Sometimes JupyterHub and its session database will get into a state
where it's very confused about the state of a user.  Usually it suffices
to:

#. Remove the user's namespace, if extant
  
#. Remove the user from the session database.  Do this with:::
  
    pod=$(kubectl get pods -n postgres | grep postgres | awk '{print $1}')
    kubectl exec -it -n postgres ${pod} -- /bin/bash -l	
    postgres-<podname>:/# psql -U jovyan jupyterhub
    delete from users where name='<user-to-remove>'
	
In some cases you may also need to remove the user from the spawner
table.  ``select * from spawners`` and find the pod with the user's name
in it, and then delete that row.
