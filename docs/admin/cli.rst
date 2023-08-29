Command-line interface
======================

Many administrative actions for Phalanx environments are being moved into a Phalanx command-line tool.
The commands for the :command:`phalanx` CLI are documented here.

You can get detailed help for any :command:`phalanx` command by running :command:`phalanx help` followed by the command (either one or two words).

.. warning::

   Phalanx does not yet use the secrets management and Vault credential management approach implemented by this tool.
   It is currently being tested and is not ready for general use.
   This warning will be removed once it is ready.

.. click:: phalanx.cli:main
   :prog: phalanx
   :nested: full
