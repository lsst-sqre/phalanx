.. px-app:: consdb

###########################################
consdb — Populate the consolidated database
###########################################

There are two parts to the consolidated database application here:
  - The ``hinfo`` service populates the ``exposure`` and ``visit`` tables,
    as well as related tables like ``ccdexposure``.
  - The ``pqserver`` service responds to publish and query requests from
    clients, allowing insertion into fixed and flexible metadata tables
    and querying of all tables and views.

.. jinja:: consdb
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
