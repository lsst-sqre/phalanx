#########################
Editing Phalanx on GitHub
#########################

The Phalanx repository is hosted on GitHub at https://github.com/lsst-sqre/phalanx.
Some types of small changes can be made directly there without having to set up a local development environment.
Other changes, however, require a development environment to make correctly.

Changes that are safe to make on GitHub
=======================================

If you wish, you can make the following classes of changes using the edit button on GitHub:

- Changing the applications settings in :file:`values-{environment}.yaml` for a specific environment (**not** :file:`values.yaml`).
- Updating the ``appVersion`` of an application in :file:`Chart.yaml`.
- Disabling or re-enabling an application for an environment in :file:`environments/values-{environment}.yaml` when the application is already configured for that environment.
- Small documentation changes where there is little risk of introducing a syntax error.

For any other changes, please set up a :doc:`local development environment <local-environment-setup>` and use it to create your PR.

Creating a PR
=============

All changes to Phalanx must be done via a pull request.
Direct changes to the ``main`` branch, even for trivial changes, are not allowed.

When you try to commit a change made on GitHub, GitHub will recognize this and prompt you to create a branch and a PR.
Before submitting, edit the proposed branch name to follow the conventions in the `LSST DM developer guide <https://developer.lsst.io/work/flow.html#git-branching>`__.

For small changes of this type, and as long as you are the developer responsible for the application whose configuration you are changing, you may merge the change without further review using the :guilabel:`Merge when ready` button on the resulting PR.
Changes will only be merged once they pass automated GitHub Actions tests.
