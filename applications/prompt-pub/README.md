# prompt-pub

Manages the lifecycle of Butler Prompt Data Products as they move from the embargo repo to publication for end users.

## Source Code

* <https://github.com/lsst-dm/prompt_publication_service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the prompt-pub statefulset pod |
| alloyDbProxy.config.instanceUri | string | `""` | Uri for Allow DB instance |
| alloyDbProxy.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the allow db proxy image |
| alloyDbProxy.image.repository | string | `"gcr.io/alloydb-connectors/alloydb-auth-proxy"` | Image to use for alloy db proxy |
| alloyDbProxy.image.tag | string | `"1.14.3"` | Tag of image to use |
| alloyDbProxy.resources | object | See `values.yaml` | Resource limits and requests for the alloy db proxy pod |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the prompt-pub image |
| image.repository | string | `"ghcr.io/lsst-dm/prompt_publication_service"` | Image to use in the prompt-pub deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| middleware.lsstResources.numWorkers | int | `4` | Sets the number of concurrent Butler file transfers per process.  Setting it explicitly here because this value is nondeterministic if you don’t assign something, but the exact value isn’t that critical. |
| middleware.lsstResources.s3ProfileEmbargo | string | `"https://sdfembs3.sdf.slac.stanford.edu"` | S3 Profile for Embargo |
| nodeSelector | object | `{}` | Node selection rules for the prompt-pub statefulset pod |
| podAnnotations | object | `{}` | Annotations for the prompt-pub statefulset pod |
| publication.butlerWriterKafka.address | string | `""` | Address to Butler Writer Kafka |
| publication.butlerWriterKafka.groupId | string | `"prompt-publication"` | Kafka Consumer Group ID |
| publication.butlerWriterKafka.topic | string | `"butler-writer-ingestion-events"` | Butler Writer Kafka Topic.  Equal to kafka.outputTopic from the butler-writer-service app |
| publication.butlerWriterKafka.username | string | `"prompt-publication-consumer"` | Kafka Consumer User Name |
| publication.embargoBatchFileDir | string | `""` |  |
| publication.repos.embargo | string | `""` | Path to Embargo Butler config |
| publication.repos.main | string | `""` | Path to Main Butler config |
| publication.repos.promptPrep | string | `""` | Path to Prompt Prep repo config |
| publication.stateDB | string | `""` | Postgres database for holding publication state |
| replicaCount | int | `1` | Number of statefulset pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the prompt-pub statefulset pod |
| tolerations | list | `[]` | Tolerations for the prompt-pub deployment pod |
