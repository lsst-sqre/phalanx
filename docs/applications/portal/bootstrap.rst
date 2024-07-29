.. px-app-bootstrap:: portal

####################
Bootstrapping Portal
####################

If the Portal Aspect is configured with a ``replicaCount`` greater than one (recommended for production installations), the ``sharedWorkarea`` volume must ultimately resolve to a volume that supports multiple simultaneous writes.
Very few Kubernetes persistent volume provisioners support ``ReadWriteMany`` (see :doc:`/applications/portal/volumes` for a more detailed discussion) so it is very likely you will need to set one of ``config.volumes.sharedWorkarea.hostPath`` or ``config.volumes.sharedWorkarea.nfs`` to achieve multi-write capability.

The IDF environments use `Google Filestore`_ via NFS.

The provisioning of either NFS or host path underlying backing store is manual, so make sure you either have created it or gotten a system administrator with appropriate permissions for your site to do so.

Ensure that it is writable by the Portal pods.
The UID for the Portal pods is 91 and is hardcoded into the Portal container image.
If UID 91 cannot be used, you will need to build your own container from https://github.com/Caltech-IPAC/firefly/blob/dev/docker/Dockerfile, specifying ``uid`` (and likely ``gid``) as a command-line argument.

