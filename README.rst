#######
Phalanx
#######

This is the Argo CD repository for the Rubin Science Platform.
It stores the root Argo CD application, deployment configuration for the other applications, the installer, and other helper scripts.

See `phalanx.lsst.io <https://phalanx.lsst.io/>`__ for the documentation.

Phalanx is developed by the `Vera C. Rubin Observatory <https://www.lsst.org/>`__.

Environments
============

The following environments are managed by Argo CD using configuration in this repository.
(The links are links to the Argo CD dashboards, which require authentication.
The names in parentheses are the environment names used internally in this repository to name values files and for other purposes.)

IDF:

* `data-dev.lsst.cloud <https://data-dev.lsst.cloud/argo-cd>`__ (idfdev)
* `data-int.lsst.cloud <https://data-int.lsst.cloud/argo-cd>`__ (idfint)
* `data.lsst.cloud <https://data.lsst.cloud/argo-cd>`__ (idfprod)

NCSA:

* `lsst-lsp-int.ncsa.illinois.edu <https://lsst-lsp-int.ncsa.illinois.edu/argo-cd>`__ (int)
* `lsst-lsp-stable.ncsa.illinois.edu <https://lsst-lsp-stable.ncsa.illinois.edu/argo-cd>`__ (stable)

Telescope and Site:

* `tucson-teststand.lsst.codes <https://tucson-teststand.lsst.codes/argo-cd>`__ (tucson-teststand)
* `base-lsp.lsst.codes <https://base-lsp.lsst.codes/argo-cd>`__ (base)
* `summit-lsp.lsst.codes <https://summit-lsp.lsst.codes/argo-cd>`__ (summit)

There are some other environments that are used for development and testing and may not be up or reachable at any given moment.

Naming
======

A phalanx is a SQuaRE deployment (Science Quality and Reliability Engineering, the team responsible for the Rubin Science Platform).
Phalanx is how we ensure that all of our services work together as a unit.
