##############
Setting quotas
##############

As part of its function as the authorization service for the Rubin Science Platform, Gafaelfawr also tracks user quotas and enforces API quotas.
Quotas are normally set in the Gafaelfawr :file:`values-{environment}.yaml` file for each environment.
They can also be temporarily overridden by using the Gafaelfawr REST API.

Types of quota
==============

Gafaelfawr tracks two types of quota for each user: API quotas and notebook quotas.
The notebook quotas are enforced by :px-app:`nublado` and only tracked in Gafaelfawr.

API quotas
----------

An API quota limits a user to a number of requests in each 15 minute interval.
After 15 minutes, the user's usage resets and they get their full quota again.

Every named service has a separate API quota.
This quota may not exist, in which case requests to that service are not rate limited.
All requests on behalf of a user count against that user's quota, whether they are made directly by the user or indirectly by another service on behalf of the user.

The scope of a "named service" for API quota purposes is the ``config.service`` key of a ``GafaelfawrIngress`` resource.
Every ``GafaelfawrIngress`` with the same ``config.service`` value consumes the API quota by the same name.

If a user is not subject to any quota for a particular service, no quota-related HTTP headers will be present in the response.
If a quota is in place, multiple ``X-RateLimit-*`` headers will be set.
See `the Gafaelfawr rate limit header documentation <https://gafaelfawr.lsst.io/user-guide/headers.html#rate-limit-headers>`__ for more details.
These headers are based on the rate limiting used by GitHub.

If the user exceeds their quota, subsequent requests will be rejected with an HTTP 429 response code.
That response will include the same ``X-RateLimit-*`` headers as well as the HTTP-standard ``Retry-After`` header, which specifies the time at which the user's quota will reset.

Notebook quotas
---------------

The user's notebook quota controls the maximum number of CPU equivalents and the maximum amount of memory that a user's notebook can use.
This, in turn, is used to filter the menu of sizes of notebooks that the user can request from the Nublado notebook spawning page.
Only sizes that fall below the user's quota will be available.

The size of the Nublado image is set as Kubernetes limits on the CPU and memory of the pod.
If the pod uses more CPU than its limit, it will be throttled.
If it uses more memory than its limit, the pod, and the user's notebook, will be terminated.
This is an abrupt experience, and it will usually not obvious to the user that this is why their notebook died.
Unfortunately, Kubernetes doesn't offer better options at present.

The requested CPU and memory, which Kubernetes uses for scheduling and node pool scale-up, are currently always set to 25% of the limits.

The notebook quota also includes a boolean flag, ``spawn``, which controls whether that user should be able to spawn new notebooks.
This flag is enforced by Nublado, not by Gafaelfawr.

Setting quotas
==============

Quotas are normally set via the ``config.quota`` key in :file:`values-{environment}.yaml` for Gafaelfawr in a given environment.
Default quotas that apply to every environment can be set in Gafaelfawr's :file:`values.yaml`.

There are three sections under the ``config.quota`` key.

Default quota
-------------

The default quota setting controls the quotas that all users get when there are no more specific rules (discussed below).
The ``api`` key should contain a mapping of service names to number of requests per 15 minutes.
The ``notebook`` key should contain ``cpu`` and ``memory`` keys specifying the default CPU and memory limits.
The memory limit is given in a floating point number of GiB.

For example:

.. code-block:: yaml

   config:
     quota:
       default:
         api:
           datalinker: 1000
         notebook:
           cpu: 2.0
           memory: 4.0

This sets a quota of 1000 requests per 15 minutes for the ``datalinker`` service, no quotas for any other API service, and a default limit of 2.0 CPU equivalents and 4.0 GiB of memory for notebooks.

The default quota for all API services not listed is unlimited.
To set a default quota of 0, explicitly list the API service with a quota of 0.

Group quota
-----------

Second, the ``groups`` key sets **additional** quota granted to members of specific groups.
The quota for every group of which the user is a member is added to the default quota.
For example:

.. code-block:: yaml

   config:
     quota:
       groups:
         g_developers:
           api:
             datalinker: 500
           notebook:
             cpu: 0.0
             memory: 4.0

If this were combined with the above default quota, members of the ``g_developers`` group would receive a total of 1500 requests per 15 minutes for datalinker, and a total of 8.0 GiB of memory for notebooks.
The CPU quota for notebooks would be unchanged.

Normally, the group quota can only add to the individual quota.
There are two exceptions: the ``spawn`` flag for notebooks, and any API quotas for services that have no default quotas.
Consider the following addditional configuration:

.. code-block:: yaml

   config:
     quota:
       groups:
         g_limited:
           api:
             tap: 1000
           notebook:
             cpu: 0.0
             memory: 0.0
             spawn: false

If combined with the previous default configuration, members of the ``g_limited`` group will have a quota of 1000 requests per 15 minutes to the tap service.
Users who are not a member of that group will continue to have unlimited access to the tap service.
Also, members of the ``g_limited`` group will not be allowed to spawn new notebooks, because their ``spawn`` flag is set to false instead of the default of true.
Note that ``cpu`` and ``memory`` are also set because they are required fields, but are set to 0.0 so they don't add anything to the quota.

Bypass groups
-------------

Finally, some groups can be allowed to bypass all quota limits.
This is done with the ``bypass`` key.

.. code-block:: yaml

   config:
     quota:
       bypass:
         - "g_admins"

All members of any group listed under ``bypass`` will ignore all quota restrictions, including the ``spawn`` flag for notebook quotas.

Overriding quotas
=================

Finally, Gafaelfawr supports temporary quota overrides.
This is done via the following REST API:

``GET /auth/api/v1/quota-overrides``
    Retrieves the current quota overrides in JSON format.
    Returns 404 if there are no quota overrides.

``PUT /auth/api/v1/quota-overrides``
    Creates or replaces the quota overrides.
    The body should be in JSON format.
    There is no ``PATCH`` API; the complete override configuration has to be provided.

``DELETE /auth/api/v1/quota-overrides``
    Delete the quota overrides.
    Returns 404 if there are no quota overrides and 204 on success.

These routes require a token with ``admin:token`` scope.
You can create such a token via the token drop-down from the front page of a Phalanx installation that uses :px-app:`squareone`.

The body sent via ``PUT`` and returned by ``GET`` is the same format as the ``config.quota`` key for the Gafaelfawr configuration except in JSON format.
The following :command:`curl` command template may be useful for setting the quota overrides:

.. prompt:: bash

   curl -X PUT -H 'Authorization: bearer <token>' \
       -H 'Content-Type: application/json' \
       -d '<json>' \
       https://<base-url>/auth/api/v1/quota-overrides

Replace ``<token>`` with your ``admin:token`` token, ``<json>`` with the content of the quota override, and ``<base-url>`` with the base URL of the Phalanx environment.

Quota overrides, unlike group quotas, are not additive.
Instead, they override (as in the name) any quota from the default or group sections.
If the quota override configuration generates a notebook quota or an API quota for a particular service, the default and group quota information for notebooks or that API are ignored completely.
Otherwise, the normal quota default and group quota information applies.

One common reason to set a quota override is to temporarily block notebook spawns.
That use is described in more detail at :doc:`/applications/nublado/block-spawns`.
