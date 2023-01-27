####################
Managing mobu flocks
####################

mobu calls each test runner a "monkey" and organizes them into groups called "flocks."
You can get a list of flocks from the mobu API.
For example, on the IDF production deployment, go to:

`https://data.lsst.cloud/mobu/summary <https://data.lsst.cloud/mobu/summary>`_

Flocks can be also manipulated through the API.
For example, to stop a noisy flock running on ``data.lsst.cloud`` while troubleshooting is in progress, first obtain a token with ``exec:admin`` scope from the authentication service, and then:

.. code-block:: bash

   curl -H 'Authorization: bearer <token>' -X DELETE https://data.lsst.cloud/mobu/flocks/tutorial
