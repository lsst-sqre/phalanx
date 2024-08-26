#######################
Communicating an Outage
#######################

Intended audience: Anyone who is administering a Rubin Science Platform environment, or covers for an administrator.

Putting up a banner
===================

The banners that appear on the RSP home page (:doc:`squareone </applications/squareone/index>`) are provided by the :doc:`semaphore </applications/semaphore/index>` service.

The content of those banners is sourced from the https://github.com/lsst-sqre/rsp_broadcast repository.
You will need push access to that repository.


.. tip::

    When changing messages on rsp_broadcast specifically you are allowed to:

    * Commit directly to main
    * Self-merge / skip review
    * "Edit on Github"

Steps:
------

1. Edit or create a message in https://github.com/lsst-sqre/rsp_broadcast/tree/main/broadcasts (if you are in a hurry and you have an issue affecting data.lsst.cloud consider editing 104_idfprod_outage.md on GitHub and committing directly to main)

2. Edit your message. If you are starting from an existing message
    a. Update the summary and body of the message (the body is what appears if the user expands
    the banner)
    b. Check the correct environment is listed in the message
    c. Set ``enabled`` to true (if you're ready for the message to go live)

3. Commit and push to ``main``. The message will immediately appear on your RSP's landing page.

4. When the emergency is over, repeat the steps above but this time edit the file to read ``enabled: false`` to take the banner down.

Here is an example of a message that will appear on data.lsst.cloud (idfprod) and data-int.lsst.cloud (idfint):

.. code-block:: yaml

    ---
    summary: Issues with catalog search from the portal
    env:
        - idfprod
        - idfint
    enabled: true
    ---

    We are aware of and are investigating an issue with DP0.2 searches in the portal

The summary appears on the banner, the body appears if the user clicks the "details" button on the banner.
See :doc:`environments </environments/index>` for the short labels for your environment.

.. seealso::

    More information about the syntax of Semaphore broadcasts messages can be found in the `rsp_broadcast README <https://github.com/lsst-sqre/rsp_broadcast/blob/main/README.md>`__.
    Information about Semaphore's installation and operation can be found in `the Semaphore documentation <https://github.com/lsst-sqre/rsp_broadcast/blob/main/README.md>`__.
    Routine banners such as the Patch Thursday messages automatically go up and down using semaphore's cron-like syntax and you should not be editing them.
    By default, banners are "scary red". For informational banners use ``category: info`` in the YAML header.

Push browser notications, per-user notifications and notifications on other RSP UIs are all on the future roadmap.

Slack
=====

If you have a slack channel for your users, post a message there.

If there is a slack status channel for your environment and it is alerting, please leave an explanation for the alert in those channels.
If the outage is likely to persist for some time, consider stopping some or all mobu flocks - see https://mobu.lsst.io/user_guide/flocks.html for more info.
