.. px-app:: weathernbeats

############################################################################
weathernbeats — Service that provides temperature based on prediction model.
############################################################################

.. jinja:: weathernbeats
   :file: applications/_summary.rst.jinja

EFD authentication
==================

At Base, the application uses ``LSST_SITE=base`` and a copy of the ``obssys``
``.efdauth.json`` secret. An init container copies the credentials into an
in-memory volume with owner UID 1000 and mode ``0600``. The application mounts
that volume read-only and receives its file path through ``EFDAUTH``.

Other environments use mock telemetry by default. To configure live EFD access,
set ``config.lsstSite``, configure ``efdCredentials``, and provide the
corresponding environment's secret definition. The EFD credential must be
synchronized to Vault before the updated pod can start.

Guides
======

.. toctree::
   :maxdepth: 1

   values
