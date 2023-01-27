.. px-app-troubleshooting:: postgres

########################
Troubleshooting postgres
########################

.. _recreate-postgres-pvc:

Recreating postgres PV/PVC
==========================

If you get into a state where the cluster has completely crashed, perhaps due to hardware problems, and the backing store for persistent volumes has been lost, Postgres may refuse to start.
The reason for this is that if you are using an autoprovisioned storage class (such as GKE and Rook provide), the PVC will reference a volume that no longer exists.
This loss is acceptable; the :px-app:`postgres` database is intended to hold only fairly low-value data.
If your cluster has crashed that hard, the authentication Redis cache and JupyterHub session database are unlikely to still be relevant.

To recover, you need to delete the PVC, recreate it (which will re-allocate the persistent storage), and restart the deployment.
This is most easily accomplished with Argo CD, although ``kubectl`` works as well.
