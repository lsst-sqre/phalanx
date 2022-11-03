.. px-app:: mobu

##############################
mobu — RSP integration testing
##############################

mobu is the continuous integration testing framework for the Rubin Science Platform.
It runs some number of "monkeys" that simulate a random user of the Science Platform.
Those monkeys are organized into "flocks" that share a single configuration across all of the monkeys.
Failures are reported to Slack using a Slack incoming webhook.

.. jinja:: mobu
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 2

   configuring
   manage-flocks
   values
