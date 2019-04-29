# Logging

This folder sets up the services required to spin up a log aggregator.

The helm charts used here are:

1. Elasticsearch - the indexer where the logs are stored
and queried from.  Elasticsearch needs persistent storage available,
but doesn't need to run on every node.

2. Fluentd - a daemonset, on every node (even dedicated
nodes).  This pod mounts the root filesystem and slurps up the logs
in various places marked in the config.  These logs are forwarded
to Elasticsearch.

3. Kibana - the frontend for searching and viewing search results.
