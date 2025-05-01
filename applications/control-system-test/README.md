# control-system-test

Deployment for the Test CSCs and Integration Testing Workflows

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.controlSystem.appNamespace | string | Set by ArgoCD | Application namespace for the control system deployment |
| global.controlSystem.imageTag | string | Set by ArgoCD | Image tag for the control system deployment |
| global.controlSystem.kafkaBrokerAddress | string | Set by ArgoCD | Kafka broker address for the control system deployment |
| global.controlSystem.kafkaTopicReplicationFactor | string | Set by ArgoCD | Kafka topic replication factor for control system topics |
| global.controlSystem.s3EndpointUrl | string | Set by ArgoCD | S3 endpoint (LFA) for the control system deployment |
| global.controlSystem.schemaRegistryUrl | string | Set by ArgoCD | Schema registry URL for the control system deployment |
| global.controlSystem.siteTag | string | Set by ArgoCD | Site tag for the control system deployment |
| global.controlSystem.topicName | string | Set by ArgoCD | Topic name tag for the control system deployment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| integration-testing.enabled | bool | `false` | Enable the integration testing system |
| rumba.enabled | bool | `false` | Enable cronjob to clean up inactivate Kafka consumers. |
| integration-testing.envEfd | string | `nil` | The Name of the EFD instance. |
| integration-testing.image.tag | string | `nil` | The image tag for the Integration Test runner container |
| integration-testing.jobLabelName | string | `"control-system-test"` | Label for jobs to get them to appear in application |
| integration-testing.persistentVolume.claimName | string | `"saved-reports"` | PVC name for saving the reports |
| integration-testing.persistentVolume.storage | string | `"1Gi"` | Storage size request for the PVC |
| integration-testing.reportLocation | string | `"/home/saluser/robotframework_EFD/Reports"` | Container location of the RobotFramework reports |
| integration-testing.s3Bucket | string | `nil` | The S3 bucket name to use |
| integration-testing.serviceAccount | string | `"integration-tests"` | This sets the service account name |
| integration-testing.workflowName | string | `"integration-test-workflow"` | Name for the top-level workflow |
| rumba.failedJobsHistoryLimit | int | `1` | The number of failed pods to keep |
| rumba.image.pullPolicy | string | `"Always"` |  |
| rumba.image.tag | string | `"latest"` | The image tag for the rumba cronjob container |
| rumba.namespace | string | `"control-system-test"` | This is the namespace in which the rumba cronjob will be placed |
| rumba.schedule | string | "*/10 * * * *" (every ten minutes) | The Schedule for executing the job to clean up inactive consumers |
| rumba.successfulJobsHistoryLimit | int | `2` | The number of succesful pods to keep |
