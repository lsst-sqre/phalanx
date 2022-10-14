##########################
Recreating postgres PV/PVC
##########################

If you get into a state where the cluster has completely crashed,
perhaps due to hardware problems, and the backing store for persistent
volumes has been lost, Postgres may refuse to start.

The reason for this is that if you are using an autoprovisioned storage
class (such as GKE and Rook provide), the PVC will reference a volume
that no longer exists.

This, in and of itself, is not a tragedy.  The Postgres database is
intended to hold only fairly low-value data.  If your cluster has
crashed that hard, the authentication Redis cache and JupyterHub session
database are unlikely to still be relevant.

All you need to do to recover is to delete the PVC, recreate it (which
will re-allocate the persistent storage), and restart the deployment.
This is most easily accomplished with ArgoCD, although ``kubectl`` works
as well.
