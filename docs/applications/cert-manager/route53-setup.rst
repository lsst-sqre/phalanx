####################################
Setting up Route 53 for cert-manager
####################################

Each domain under which ``cert-manager`` needs to issue certificates must be configured in AWS.
This involves creating a new hosted zone for the DNS challenges for that domain, creating an AWS service user with an appropriate IAM policy, and creating an access key for that user which will be used by ``cert-manager``.

Normally, DNS challenges work by writing a text record to the ``_acme-challenge.<hostname>`` record for the hostname for which one is obtaining a certificate.
However, Route 53 IAM policies are only granular to the level of a hosted zone.
To give ``cert-manager`` write access to the whole hosted zone would be excessive, since it could then modify any other records.
Therefore, we use a strategy documented in the `cert-manager documentation for Route 53 <https://cert-manager.io/docs/configuration/acme/dns01/route53/>`__ to delegate only the relevant records.

To do this for a new zone, do the following.
In these instructions, the new zone is shown as :samp:`new.zone`.
In practice this will be a zone like ``lsst.codes`` or ``lsst.cloud``.
This must be a public domain served from normal Internet domain servers.
It cannot be a private domain present only in Route 53.

#. Create a new hosted zone named :samp:`tls.{new.zone}` in Route 53.
   Make a note of its zone ID.

#. Add the NS glue record for :samp:`tls.{new.zone}` to :samp:`{new.zone}` in Route 53.
   See `the Route 53 documentation <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-routing-traffic-for-subdomains.html#dns-routing-traffic-for-subdomains-creating-records>`__ for more details.

#. Create a new IAM user named :samp:`cert-manager-{new-zone}` (replace ``new-zone`` with the name of your zone).
   Attach an inline IAM policy for that user that gives it access to the new :samp:`tls.{new.zone}` hosted zone.

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

   Replace :samp:`{<zone-id>}` with the ID of the hosted zone
   (which is a string looking like ``Z0567328105IEHEMIXLCO``.)

#. Create an access key for that user.
   Store the access key and secret key pair in 1Password as :samp:`cert-manager-{new-zone}`.

You can now follow the instructions in :px-app-bootstrap:`cert-manager` to set up the new cluster.

The above instructions only have to be done once per domain.
After that, any new clusters in the same domain will only need the addition of a CNAME and some Vault and Argo CD configuration, as described in :px-app-bootstrap:`cert-manager`.

Dedicated ServiceAccount authentication on GKE
==============================================

The ``idfdev``, ``idfprod``, ``idfint``, ``roundtable-dev``, and ``roundtable-prod`` environments use dedicated Kubernetes ServiceAccount authentication instead of static AWS credentials.
Their ``config.route53.roleArn`` values are placeholders and must be replaced before deployment.
The AWS region is ``us-east-1`` for both authentication methods.

Register the GKE cluster's OIDC issuer as an AWS IAM OIDC provider with the audience ``sts.amazonaws.com``.
Create an IAM role with the Route 53 permissions shown above and a trust policy permitting ``sts:AssumeRoleWithWebIdentity`` from that provider.
Restrict the trust policy to the subject ``system:serviceaccount:cert-manager:cert-manager-route53`` and audience ``sts.amazonaws.com``.
If deploying into another namespace, adjust the subject accordingly.
See the `dedicated ServiceAccount documentation <https://cert-manager.io/docs/configuration/acme/dns01/route53/#iam-role-with-dedicated-kubernetes-serviceaccount>`__ for details.

Set ``config.route53.roleArn`` to the role ARN and remove ``config.route53.awsAccessKeyId`` from the environment values.
The chart creates the ``cert-manager-route53`` ServiceAccount and grants the cert-manager controller permission to request tokens only for that account.
For a ClusterIssuer, this account must be in cert-manager's cluster resource namespace, which defaults to the controller namespace.
The chart places it in the release namespace; keep the cluster resource namespace at that default.
No AWS credentials need to be stored in Vault for this mode.

To use static credentials instead, leave ``config.route53.roleArn`` empty, set ``config.route53.awsAccessKeyId``, and provision ``aws-secret-access-key`` as described above.
