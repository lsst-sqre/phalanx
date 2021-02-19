# Phalanx

This is the repository to store helper scripts and per-environment
deployment configuration for the services of the Rubin Science
Platform.

For operational documentation, see [phalanx.lsst.io](https://phalanx.lsst.io/).

## Background

In order to understand this repository, there's a bit of background
and layering that needs to be understood.  I will briefly cover each
layer here, and link to further documentation if you are interested.

The Rubin Science Platform runs on Kubernetes (https://kubernetes.io/).
Kubernetes provides a way to coordinate running services on multiple
nodes.  Kubernetes runs a set of docker containers (https://docker.com/),
and sets up the networking, storage, and configuration of those containers.

Git repositories for individual services typically have build pipelines
resulting in new docker container builds when code changes are merged.
For example, our Jenkins build system builds stack and JupyterLab containers,
and the lsst-tap-service repository builds the TAP service containers,
and so on.

Kubernetes generally works by handling Kubernetes resources like pods,
deployments, and services.  But many of these resources need to be configured
to work together to form a logical service, such as Firefly or Nublado. Each
logical application is contained in a Helm chart (https://helm.sh) that
uses templates to create each resource with some configuration applied.
The configuration for a helm chart is called a values file, and is a simple
YAML document that contains inputs for the templating of the chart.  Each
environment has its own YAML document containing the required configuration
for that chart.

But Helm doesn't keep track of the application once it is deployed.  That is,
it won't notice when the configuration changes and apply those changes.
ArgoCD (https://argoproj.github.io/argo-cd/) fills this need.  ArgoCD watches
this repository for new git commits and will keep track of those changes,
either applying them automatically ("syncing" them), or waiting for an operator
to press the sync button in the web UI.  ArgoCD is the only layer in this
stack that has a web UI that can be easily navigated, and it provides many
useful features, such as deleting resources and resyncing applications.

Now, this is great, because everything is checked into git.  But many service
configurations require some secrets such as random numbers, certificates, or
passwords.  But we can't obviously check those into a public repository.  This
is where Vault (https://www.vaultproject.io/) comes in.  Some of the helm values
files contain paths to keys in our vault installation, located at
https://vault.lsst.codes.  Each environment is seeded with a key that it
uses to access secrets in the vault and make them available for the services
to read.

## Repository Layout

While ArgoCD can be used and configured in any number of ways, there is also
a layer of convention to simplify and add some structure that works for us
to deploy the science platform services.

First, there is the installer directory.  This directory contains a script,
called install.sh.  The arguments to this are the name of the environment,
the FQDN, and the read key for https://vault.lsst.codes.  This installer
script is the entrypoint for setting up a new environment, and should be
able to be run even on an existing environment to update it.

Next, there is the services directory.  Each sub-directory in services is
one service of the Rubin Science Platform.  This directory contains helm
values files for each of the environments that use that component, and
specify which helm chart to use to deploy that service.  Each of the
values files are named values-environment.yaml.

Finally, there is the science-platform directory.  This contains an argocd
application that specifies which services an environment should use, and
creates all those services in argocd.  The values files in this directory
contain the service manifest and other top level configuration.

## How to use this repository

Okay now that we understand the tools used, and the various conventions
("The forms MUST be obeyed..."), we can get into how to use this repository
to manage environments and services.

There are already a number of different environments reflecting our many
different deployments, such as int and stable, base, and summit.
There are also a number of teststands used not for software testing but
hardware testing, such as tucson teststand (TTS) and NCSA teststand (NTS).
Finally there are software test environments.  New environments can be
added by generally cargo-culting the current test environments and
tweaking them as necessary.

If you aren't adding a new environment, you might be adding a new service.
Add a directory with the service name (generally corresponding to the chart
name), and add the appropriate values files inside.  Then you can cargo-cult
the science-platform app to add a new application and the various configuration
on / off switches per environment.

If you aren't adding a new environment or a service, it is likely that you are
changing the configuration for a service, or rolling out a new version.
Since the versions (which correspond to docker tag names usually) are
treated as configuration data, there is really only updating configuration
data.  This is done by making a PR to this repository and editing the
values files of the services to change the configuration.

In general, this should be done only as needed and where needed.  When
rolling out a service update all the way to stable, it should be commited
up to int, tested, and then a new PR for the version upgrade to stable.
When these values files are updated, the ArgoCD dashboard will show as
out of sync.  The sync button can then be pressed in the UI to deploy
the configuration change.

Sometimes, a change to the helm charts is also required.  The square
helm charts are found at https://github.com/lsst-sqre/charts .  Once
that PR is merged, the chart is published via a github action, and then
ArgoCD will poll the chart URL to find a new chart.

Once your ArgoCD says you are green, then you are where you say you
want to be.  If something happens to the cluster and its resources,
ArgoCD will let you know, even the action wasn't taken by ArgoCD.
This makes it useful for reverting back to a LKG (Last-Known-Good)
state.

## Naming

A phalanx is a SQuaRE deployment (Science Quality and Reliability
Engineering, the team responsible for the Rubin Science Platform).
Phalanx is how we ensure that all of our services work together as a unit.
