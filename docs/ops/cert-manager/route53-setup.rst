####################################
Setting up Route 53 for cert-manager
####################################

Each domain under which ``cert-manager`` needs to issue certificates must be configured in AWS.
This involves creating a new hosted zone for the DNS challenges for that domain, creating an AWS service user with an appropriate IAM policy, and creating an access key for that user which will be used by ``cert-manager``.

Normally, DNS challenges work by writing a text record to the ``_acme-challenge.<hostname>`` record for the hostname for which one is obtaining a certificate.
However, Route 53 IAM policies are only granular to the level of a hosted zone.
To give ``cert-manager`` write access to the whole hosted zone would be exessive, since it could then modify any other records.
Therefore, we use a strategy documented in the `cert-manager documentation for Route 53 <https://cert-manager.io/docs/configuration/acme/dns01/route53/>`__ to delegate only the relevant records.

To do this for a new zone, do the following.
In these instructions, the new zone is shown as ``new.zone``.
In practice this will be a zone like ``lsst.codes`` or ``lsst.cloud``.
This must be a public domain served from normal Internet domain servers.
It cannot be a private domain present only in Route 53.

#. Create a new hosted zone named ``tls.new.zone`` in Route 53.
   Make a note of its zone ID.

#. Add the NS glue record for ``tls.new.zone`` to ``new.zone`` in Route 53.
   See `the Amazon documentation <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-routing-traffic-for-subdomains.html#dns-routing-traffic-for-subdomains-creating-records>`__ for more details.

#. Create a new IAM user named ``cert-manager-new-zone``.
   (Don't forget to replace ``new-zone`` with the name of your zone.)
   Attach an inline IAM policy for that user that gives it access to the new ``tls.new.zone`` hosted zone.

   .. code-block:: json

      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Sid": "VisualEditor0",
                  "Effect": "Allow",
                  "Action": "route53:GetChange",
                  "Resource": "arn:aws:route53:::change/*"
              },
              {
                  "Sid": "VisualEditor1",
                  "Effect": "Allow",
                  "Action": [
                      "route53:ChangeResourceRecordSets",
                      "route53:ListResourceRecordSets"
                  ],
                  "Resource": "arn:aws:route53:::hostedzone/<zone-id>"
              }
          ]
      }

   replacing ``<zone-id>`` with the ID of the hosted zone.
   (This will be a string similar to ``Z0567328105IEHEMIXLCO``.)

#. Create an access key for that user.
   Store the access key and secret key pair in 1Password as ``cert-manager-new-zone``.

You can now follow the instructions in :doc:`bootstrapping` to set up the new cluster.

The above instructions only have to be done once per domain.
After that, any new clusters in the same domain will only need the addition of a CNAME and some Vault and Argo CD configuration, as described in :doc:`bootstrapping`.
