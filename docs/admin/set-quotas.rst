##############
Setting quotas
##############

Phalanx currently supports quotas for API services and for notebook spawning.
The quotas for notebook spawning can also be used to temporarily disable spawning of new notebooks.

Quotas are configured in the application configuration for Gafaelfawr (see :px-app:`gafaelfawr`).

Gafaelfawr calculates the quota for users and returns it via the ``/auth/api/v1/user-info`` REST API, which is used by Nublado (see :px-app:`nublado`) to limit the available notebook sizes and decide whether a user is allowed to spawn a notebook.
It also enforces API quotas directly, rejecting requests with an HTTP 429 error after the user has exceeded their quota.

See :doc:`/applications/gafaelfawr/quotas` for how to configure quotas.

See :doc:`/applications/nublado/block-spawns` for how to use quotas to block spawning of new notebooks.
