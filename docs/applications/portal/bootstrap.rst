.. px-app-bootstrap:: portal

####################
Bootstrapping Portal
####################

If the Portal Aspect is configured with a ``replicaCount`` greater than one (recommended for production installations), ``config.volumes.workareaHostPath`` or ``config.volumes.workareaNfs`` must be set and point to an underlying filesystem that supports shared multiple-write.
This is not supported by most Kubernetes persistent volume backends, which is why only a host path or an NFS mount are supported.

The IDF environments use `Google Filestore`_ via NFS.

The provisioning of this underlying backing store is manual, so make sure you either have created it or gotten a system administrator with appropriate permissions for your site to do so.

Ensure that it is writable by the Portal pods.
The default UID for the Portal pods is 91.
If this needs to be changed, you'll need to add a new ``values.yaml`` parameter and plumb it through to the ``Deployment`` configuration.
