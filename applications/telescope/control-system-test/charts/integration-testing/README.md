# integration-testing

Helm chart for Integration Testing Workflows.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| envEfd | string | `nil` | The Name of the EFD instance. |
| image.tag | string | `nil` | The image tag for the Integration Test runner container |
| jobLabelName | string | `"control-system-test"` | Label for jobs to get them to appear in application |
| persistentVolume.claimName | string | `"saved-reports"` | PVC name for saving the reports |
| persistentVolume.storage | string | `"1Gi"` | Storage size request for the PVC |
| reportLocation | string | `"/home/saluser/robotframework_EFD/Reports"` | Container location of the RobotFramework reports |
| s3Bucket | string | `nil` | The S3 bucket name to use |
| serviceAccount | string | `"integration-tests"` | This sets the service account name |
| workflowName | string | `"integration-test-workflow"` | Name for the top-level workflow |
