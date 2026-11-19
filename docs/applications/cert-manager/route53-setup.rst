####################################
Setting up Route 53 for cert-manager
####################################

Each domain under which ``cert-manager`` needs to issue certificates must be configured in AWS.
This involves creating a new hosted zone for the DNS challenges for that domain and configuring ``cert-manager`` to be able to authenticate to AWS to update records in that domain.

Normally, DNS challenges work by writing a text record to the ``_acme-challenge.<hostname>`` record for the hostname for which one is obtaining a certificate.
However, Route 53 IAM policies are only granular to the level of a hosted zone.
To give ``cert-manager`` write access to the whole hosted zone would be excessive, since it could then modify any other records.
Therefore, we use a strategy documented in the `cert-manager documentation for Route 53 <https://cert-manager.io/docs/configuration/acme/dns01/route53/>`__ to delegate only the relevant records.

To set up a new zone for this in AWS, apply the following Terraform config (or manually do the equivalent).
This assumes that the primary hosted zone (like ``lsst.cloud``) is already created.

.. code-block:: terraform

   terraform {
     required_version = ">= 1.5.0"

     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 6.0"
       }
     }
   }

   provider "aws" {
     region = "us-east-1"
   }

   # This is the domain that certs will be provisioned for.
   variable "primary_hosted_zone_url" {
     description = "DNS name of the primary Route 53 hosted zone."
     type        = string
     default     = "lsst.codes"
   }

   locals {
     primary_hosted_zone_name = trimsuffix(var.primary_hosted_zone_url, ".")
     challenge_hosted_zone_name = "tls.${local.primary_hosted_zone_name}"
     challenge_hosted_zone_slug = replace(local.challenge_hosted_zone_name, ".", "-")
   }

   # Look up the existing primary hosted zone.
   data "aws_route53_zone" "primary" {
     name         = local.primary_hosted_zone_name
     private_zone = false
   }

   # Create the DNS-01 challenge hosted zone. This is the hosted zone where
   # cert-manager will create and modify a TXT record.
   resource "aws_route53_zone" "challenge_hosted_zone" {
     name = local.challenge_hosted_zone_name
   }

   # Delegate the challenge subdomain from the primary hosted zone.
   # See https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-routing-traffic-for-subdomains.html#dns-routing-traffic-for-subdomains-creating-records for more details.
   resource "aws_route53_record" "challenge_hosted_zone_ns" {
     zone_id = data.aws_route53_zone.primary.zone_id
     name    = aws_route53_zone.challenge_hosted_zone.name
     type    = "NS"
     ttl     = 300
     records = aws_route53_zone.challenge_hosted_zone.name_servers
   }

   # Create an IAM role to use for federated access by the cert-manager
   # Kubernetes service account for clusters that support OIDC federation.
   # The initial trust policy statement is just a placeholder. We will add
   # statements for each cluster from which we want to assume this role.
   resource "aws_iam_role" "cert_manager" {
     name                 = "phalanx-cert-manager-${local.challenge_hosted_zone_slug}"
     description          = "Route 53 DNS-01 access for ${local.challenge_hosted_zone_name}"
     max_session_duration = 3600

     assume_role_policy = jsonencode({
       Version = "2012-10-17"
       Statement = [
         {
           Sid    = "Placeholder"
           Effect = "Allow"
           Action = "sts:AssumeRole"

           Principal = {
             Service = "lambda.amazonaws.com"
           }

           Condition = {
             Bool = {
               "aws:PrincipalIsAWSService" = "false"
             }
           }
         }
       ]
     })
   }

   # Create an IAM identity-based policy that grants permissions to create TXT
   # records in the challenge zone.
   resource "aws_iam_policy" "cert_manager_route53" {
     name        = "phalanx-cert-manager-${local.challenge_hosted_zone_slug}-dns01"
     description = "Route 53 DNS-01 permissions for cert-manager in ${local.challenge_hosted_zone_name}"

     policy = jsonencode({
       Version = "2012-10-17"
       Statement = [
         {
           Sid      = "ReadChangeStatus"
           Effect   = "Allow"
           Action   = "route53:GetChange"
           Resource = "arn:aws:route53:::change/*"
         },
         {
           Sid      = "ListRecordsInChallengeZone"
           Effect   = "Allow"
           Action   = "route53:ListResourceRecordSets"
           Resource = aws_route53_zone.challenge_hosted_zone.arn
         },
         {
           Sid      = "ChangeTXTRecordsInChallengeZone"
           Effect   = "Allow"
           Action   = "route53:ChangeResourceRecordSets"
           Resource = aws_route53_zone.challenge_hosted_zone.arn

           Condition = {
             "ForAllValues:StringEquals" = {
               "route53:ChangeResourceRecordSetsRecordTypes" = ["TXT"]
             }
           }
         }
       ]
     })
   }

   # Attach this policy to the role.
   resource "aws_iam_role_policy_attachment" "cert_manager_route53" {
     role       = aws_iam_role.cert_manager.name
     policy_arn = aws_iam_policy.cert_manager_route53.arn
   }

   # Create an IAM group to contain IAM users for integrations that can't use
   # ServiceAccount federation.
   resource "aws_iam_group" "cert_manager_route53" {
     name = "phalanx-cert-manager-${local.challenge_hosted_zone_slug}-dns01"
   }

   # Attach the policy to the group.
   resource "aws_iam_group_policy_attachment" "cert_manager_route53" {
     group      = aws_iam_group.cert_manager_route53.name
     policy_arn = aws_iam_policy.cert_manager_route53.arn
   }

   # Use this in all Phalanx cert-manager config.
   output "challenge_hosted_zone_id" {
     description = "Route 53 hosted zone ID for DNS-01 challenges."
     value       = aws_route53_zone.challenge_hosted_zone.zone_id
   }

   # Use this in Phalanx cert-manager config for clusters that can do
   # ServiceAccount federation.
   output "cert_manager_role_arn" {
     description = "IAM role ARN for cert-manager."
     value       = aws_iam_role.cert_manager.arn
   }

   # Create IAM users and put them into this group for clusters that can't do
   # ServiceAccount federation.
   output "cert_manager_group_name" {
     description = "IAM group with Route 53 DNS-01 permissions."
     value       = aws_iam_group.cert_manager_route53.name
   }

After folloing either the federated or static authentication instructions, follow the instructions in :px-app-bootstrap:`cert-manager` to set up the new cluster.

These instructions only have to be done once per domain.
After that, any new clusters in the same domain will only need the addition of a CNAME and some Vault and Argo CD configuration, as described in :px-app-bootstrap:`cert-manager`.

Federated AWS authentication
----------------------------

If at all possible, ``cert-manager`` should be configured to authenticate to AWS without using long-lived static credentials.
One way to achieve this is by using a `dedicated Kubernetes ServiceAccount <https://cert-manager.io/docs/configuration/acme/dns01/route53/#iam-role-with-dedicated-kubernetes-serviceaccount>`__ and a `AWS OIDC IAM identity provider <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html>`__.
This will be possible for any Kubernetes cluster with a publicly accessible OIDC discovery endpoint that advertises a publicly accessible ``jwks_uri`` URI.
All GKE clusters with publicly accessible API endpoints meet this criteria.

Here is how you would configure this in AWS for ``cert-manager`` in the GKE ``idfdev`` cluster to create challenge records in the ``tls.lsst.cloud`` zone.

#. Get the issuer from the cluster's OIDC discovery endpoint.

   .. code-block::

      $ curl --silent 'https://container.googleapis.com/v1/projects/science-platform-dev-7696/locations/us-central1/clusters/rsp-dev/.well-known/openid-configuration' | jq '{issuer}'

      {
        "issuer": "https://container.googleapis.com/v1/projects/science-platform-dev-7696/locations/us-central1/clusters/rsp-dev"
      }

#. Create an OIDC IAM identity provider in AWS.
   Set the Provider URL to the issuer you just found, and the audience to ``sts.amazonaws.com``.

   .. code-block::

    aws iam create-open-id-connect-provider \
      --url https://container.googleapis.com/v1/projects/science-platform-dev-7696/locations/us-central1/clusters/rsp-dev \
      --client-id-list sts.amazonaws.com \
      --tags \
        Key=Name,Value=phalanx-idfdev \
        Key=Environment,Value=idfdev

#. Add this statement to the list of statements in the trust policy (NOT the attached identity-based policy) of the cert-manager role.
   You can replace the placeholder statement if it is still declared.

   .. code-block:: json

      {
          "Sid": "idfdev",
          "Effect": "Allow",
          "Principal": {
              "Federated": "arn:aws:iam::039289279626:oidc-provider/container.googleapis.com/v1/projects/science-platform-dev-7696/locations/us-central1/clusters/rsp-dev"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
              "StringEquals": {
                  "container.googleapis.com/v1/projects/science-platform-dev-7696/locations/us-central1/clusters/rsp-dev:aud": "sts.amazonaws.com",
                  "container.googleapis.com/v1/projects/science-platform-dev-7696/locations/us-central1/clusters/rsp-dev:sub": "system:serviceaccount:cert-manager:cert-manager-route53"
              }
          }
      }

Revoking federated access
^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to revoke AWS access for a ``cert-manager`` installation using this federated access, remove the statement for that cluster from the IAM role trust policy.
You may then want to destroy the AWS OIDC provider for that cluster if you want to revoke all federated `ServiceAccount` access from that cluster.

Static AWS authentication
-------------------------

If your cluster does not have public OIDC discovery endpoints, you can create an IAM user and generate an access key.

#. Create a new IAM user named :samp:`cert-manager-{new-zone}` (replace ``new-zone`` with the name of your zone).

# Place that user into the :samp:`phalanx-cert-manager-{new-zone}-dns01` IAM group.

#. Create an access key for that user.
   Store the access key and secret key pair in 1Password as :samp:`cert-manager-{new-zone}`.

Revoking static access
^^^^^^^^^^^^^^^^^^^^^^

If you need to revoke AWS access for a ``cert-manager`` installation using this static access, disable the access key for the cluster's IAM user.
Delete the IAM user if you don't plan on restoring access.
