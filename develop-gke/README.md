# Instructions for deploying the LSST Science Platform to Google Kubernetes Engine

These are instructions for how to deploy the LSST Science Platform to an existing
cluster in the Google Kubernetes Engine feature of Google Cloud.

## Creating your cluster

First, create a cluster in GKE.  You can follow these instructions from Google
here:

https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-cluster

You can either use the web console or the gcloud command line utility.

### Suggested size and settings

With the default settings provided in this directory, it is suggested
to create a cluster of at least 3 nodes, with each node having 4 vCPUs.

Disk space is also important to store docker images.  Select more options
and make sure the boot disk storage is at least 200 GB for these default
settings.

### Verifying your cluster

Before proceeding, you need to be able to connect to your cluster using the
kubectl command.  If you type:

```
kubectl get all -A
```

It should return a list of resources.  If it does not, then you must fix
this before being able to proceed to the next step.

## Installing Helm

Helm is the software that will create the services in your kubernetes
cluster.  You can learn more about helm at https://helm.sh/

If you have not yet installed helm, you can install it following
the directions found at https://github.com/helm/helm/releases for
a release.

Once you have installed helm, you should be able to run:

```
helm
```

This will display help text for helm.

### Installing tiller

Tiller is the server side component of helm.  Tiller runs in your
kubernetes cluster as a service, and helm contacts this service to
install, uninstall, and update software on your behalf.

To install tiller, run the command below in the same directory as
this README.md.

```
./install_tiller.sh
```

This script will install tiller, using slightly more security than
a normal installation, since this is on the public internet.  For
your specific use cases, you may want to look into the following
page about securing helm.  ```install_tiller.sh``` uses the RBAC
method described to specify a service account.

https://helm.sh/docs/using_helm/#securing-your-helm-installation

Note: This should be considered insecure.  Set up TLS certificate
verification as helm says when running the ```install_tiller.sh```
on a production cluster.

### Verifying helm

At this point, you should be able to run:

```
helm version
```

This should return the versions of helm running locally and
tiller in the cluster.  If it does not, do not continue.

## Installing the LSST Science Platform

The LSST Science Platform is a set of helm charts that are
configured from the yaml files in this directory.  These
values can be configured further by editing the YAML files,
although the yaml files checked in should provide a working
platform to start with.

Now you can run:

```
./install_lsp.sh
```

This script calls helm to install each chart.  This will
create kubernetes resources like pods that run each service.
