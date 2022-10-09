############################
Upgrade windows and sequence
############################

Phalanx provides configurations for multiple environments.
Many of these are production environments that service different user groups.
Other environments are intended for development and integration.

In general, new and updated services should be rolled out to development and integration environments before production environments.

Production environments also generally have specific maintenance windows when upgrades can occur.

SQuaRE environments
===================

In the case of environments managed by SQuaRE, the process for gated updates to environments is canonically defined in :sqr:`056`, but also summarized here.

The sequence for rolling out updates is:

* ``data-dev.lsst.cloud``
* ``data-int.lsst.cloud``
* ``tucson-teststand.lsst.codes``
* ``data.lsst.cloud``
* ``base-lsp.lsst.codes``
* ``summit-lsp.lsst.codes``

See :sqr:`056` for the change coordination and upgrade windows (as relevant) for each environment.
