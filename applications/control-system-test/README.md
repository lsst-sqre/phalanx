# control-system-test

Deployment for the Test CSCs and Integration Testing Workflows

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.controlSystemAppNamespace | string | Set by ArgoCD | Application namespacce for the control system deployment |
| global.controlSystemImageTag | string | Set by ArgoCD | Image tag for the control system deployment |
| global.controlSystemKafkaBrokerAddress | string | Set by ArgoCD | Kafka broker address for the control system deployment |
| global.controlSystemS3EndpointUrl | string | Set by ArgoCD | S3 endpoint (LFA) for the control system deployment |
| global.controlSystemSchemaRegistryUrl | string | Set by ArgoCD | Schema registry URL for the control system deployment |
| global.controlSystemSiteTag | string | Set by ArgoCD | Site tag for the control system deployment |
| global.controlSystemTopicName | string | Set by ArgoCD | Topic name tag for the control system deployment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| csc_collector.secrets | list | `[]` | This section holds secret specifications. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the secret) _key_ (The key in the vault store where the secret resides) _type_ (OPTIONAL: The secret type. Defaults to Opaque.) |
| integration-testing.enabled | bool | `false` | Enable the integration testing system |
| integration-testing.envEfd | string | `nil` | The Name of the EFD instance. |
| integration-testing.image.tag | string | `nil` | The image tag for the Integration Test runner container |
| integration-testing.persistentVolume.claimName | string | `"saved-reports"` | PVC name for saving the reports |
| integration-testing.persistentVolume.storage | string | `"1Gi"` | Storage size request for the PVC |
| integration-testing.reportLocation | string | `"/home/saluser/robotframework_EFD/Reports"` | Container location of the RobotFramework reports |
| integration-testing.s3Bucket | string | `nil` | The S3 bucket name to use |
| integration-testing.serviceAccount | string | `"integration-tests"` | This sets the service account name |
| integration-testing.workflowName | string | `"integration-test-workflow"` | Name for the top-level workflow |
