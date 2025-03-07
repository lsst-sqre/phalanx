.. px-app:: next-visit-fan-out-keda

################################################################################
next-visit-fan-out — Distribute next visit events for Keda
################################################################################

The next-visit-fan-out application pulls next visit events from Kafka and duplicates and fans out the events to other components that need to receive them.  This is a temporary instance for Keda testing.

.. jinja:: next-visit-fan-out-keda
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values