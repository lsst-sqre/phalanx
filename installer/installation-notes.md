# Installing the RSP

## Preparation

  * Create a working dir.
  * git clone https://github.com/lsst-sqre/phalanx into it (using https
    rather than git+ssh is important).
  * cd phalanx/installer

## Create installation environment

  * If you don't have a virtualenv for the installer already,
    `mkvirtualenv -p $(which python3) -r requirements.txt installer`
    (adjust if you use pyenv or raw virtualenv or whatever; the
    important thing is to pick up the requirements.txt from the
    installer directory)
  * Get the correct write token for this instance's Vault enclave out of
    1Password

## Prepare for the ingress

There are three cases (thus far) for what the top-level ingress looks
like.

  * It is externally managed, as are any required TLS certificates.
    The installer doesn't cope with this case very well yet, and you
    will need to manually inject the TLS certificate into the squareone
    configuration post-installation.

  * For each of the second and third, which are the cases the installer
    script is designed to support, the RSP manages the top-level
    ingress, and Let's Encrypt is used to manage TLS certificates.  The
    difference between these cases is that one has a pre-defined fixed
    IP address (e.g. the T&S sites), and one uses whatever the
    Kubernetes provider gives up (e.g. GKE).

  * In the second case, now is a good time to make sure that the top-level
    endpoint (e.g. "tucson-teststand.lsst.codes") resolves to the
    correct IP address, whether directly as an A record or as a CNAME to
    an A record.

  * For the third case you will set up the DNS record once you know the
    IP address of the endpoint.

If this is the first time you've installed the RSP in a given domain,
and you are managing TLS certs via Let's Encrypt for the RSP instance,
you will need to put a glue record into that domain to allow Let's
Encrypt to work its magic.  This process is documented at
https://phalanx.lsst.io/ops/cert-issuer/route53-setup.html for Route
53.  If you're not using Route 53, you're on your own, but use that
document as a guide for the tasks you will need to perform.

## Pre-flight check

Check the rest of the phalanx definitions.  Particular items of
 interest:
 
   * NFS mountpoints in nublado2 and moneypenny
   
   * If the Firefly portal has a replicaCount greater than one, it is
     imperative that `firefly_shared_workdir` be set and that it reside
     on an underlying filesystem that supports shared multiple-write.
     At GKE, this is currently Filestore (therefore NFS), and at NCSA,
     it is currently a hostPath mount to underlying GPFS.  Currently the
     provisioning of this underlying backing store is manual, so make
     sure you either have created it, or gotten a system administrator
     with appropriate permissions for your site to do so.  The default
     UID for Firefly is 91, although it is tunable in the deployment if
     need be.
     
   * For T&S sites that require instrument control, make sure you have
     any Multus network definitions you need for nublado2.

## Perform the installation

`./install.sh <environment> <token>`

(where "environment" looks like "tucson-teststand"--it must match a
filename in ../science-platform/values-<environment>.yaml, and "token"
is the Vault write token you got out of 1Password.

### Set up DNS record for dynamically-assigned ingress

If you are relying on the Kubernetes hosting machinery to assign an IP
address for your endpoint, while the installer is running, wait until
the ingress-nginx-controller service comes up and has an external IP
address; then go set the A record for your endpoint to that address (or
set an A record with that IP address for the ingress and a CNAME from
the endpoint to the A record).

## Wait for service availability

Now all you should need to do is wait until everything comes up and
cachemachine finishes pulling its prepulled images; you can watch the
progress either through kubectl or argocd.
