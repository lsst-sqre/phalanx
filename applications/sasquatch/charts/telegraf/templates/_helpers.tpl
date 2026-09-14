{{/* Convert a list to a TOML array of quoted string values. */}}
{{- define "telegraf.toTomlArray" -}}
{{- $items := list -}}
{{- range . -}}
{{- $items = (quote .) | append $items -}}
{{- end -}}
[ {{ join ", " $items }} ]
{{- end }}

{{/* Validate Kafka topic discovery configuration. */}}
{{- define "telegraf.validateTopicDiscovery" -}}
{{- $topicDiscovery := default dict .value.topicDiscovery -}}
{{- if (default false $topicDiscovery.enabled) -}}
  {{- $includePrefixes := default list $topicDiscovery.includePrefixes -}}
  {{- if eq (len $includePrefixes) 0 -}}
    {{- fail (printf "kafkaConsumers.%s.topicDiscovery.includePrefixes must contain at least one prefix" .key) -}}
  {{- end -}}
  {{- range $name, $prefixes := dict "includePrefixes" $includePrefixes "excludePrefixes" (default list $topicDiscovery.excludePrefixes) -}}
    {{- range $index, $prefix := $prefixes -}}
      {{- if not (kindIs "string" $prefix) -}}
        {{- fail (printf "kafkaConsumers.%s.topicDiscovery.%s[%d] must be a string" $.key $name $index) -}}
      {{- end -}}
      {{- if or (eq (trim $prefix) "") (ne $prefix (trim $prefix)) (contains "\n" $prefix) (contains "\r" $prefix) -}}
        {{- fail (printf "kafkaConsumers.%s.topicDiscovery.%s[%d] must be a non-empty prefix without surrounding whitespace or newlines" $.key $name $index) -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
  {{- $refreshInterval := default "30s" $topicDiscovery.refreshInterval -}}
  {{- if not (regexMatch "^[1-9][0-9]*[smh]$" $refreshInterval) -}}
    {{- fail (printf "kafkaConsumers.%s.topicDiscovery.refreshInterval must be a positive duration ending in s, m, or h" .key) -}}
  {{- end -}}
{{- end -}}
{{- end }}

{{/* Render a Telegraf Kafka consumer input. */}}
{{- define "telegraf.kafkaConsumer" }}
{{- $dataFormat := default "avro" .value.data_format }}
{{- if and (ne $dataFormat "avro") (ne $dataFormat "json_v2") }}
{{- fail (printf "unsupported data_format %q for %s; expected avro or json_v2" $dataFormat .consumerGroup) }}
{{- end }}
    [[inputs.kafka_consumer]]
      brokers = [
        "sasquatch-kafka-brokers.sasquatch:9092"
      ]
      consumer_group = {{ .consumerGroup | quote }}
      sasl_mechanism = "SCRAM-SHA-512"
      sasl_password = "$TELEGRAF_PASSWORD"
      sasl_username = "telegraf"
      data_format = {{ $dataFormat | quote }}
      {{- if .useTopics }}
      topics = __DISCOVERED_TOPICS__
      {{- else }}
      topic_regexps = {{ include "telegraf.toTomlArray" .value.topicRegexps }}
      {{- end }}
      offset = {{ .offset | quote }}
      precision = {{ default "1us" .value.precision | quote }}
      max_processing_time = {{ default "1s" .value.max_processing_time | quote }}
      consumer_fetch_default = {{ default "1MB" .value.consumer_fetch_default | quote }}
      max_undelivered_messages = {{ default 10000 .value.max_undelivered_messages }}
      compression_codec = {{ .compressionCodec }}
      kafka_version = {{ .kafkaVersion | quote }}
      {{- if eq $dataFormat "avro" }}
      avro_schema_registry = {{ default "http://sasquatch-schema-registry.sasquatch:8081" .registryUrl | quote }}
      {{- if .timestampField }}
      avro_timestamp = {{ .timestampField | quote }}
      avro_timestamp_format = {{ default "unix" .value.timestamp_format | quote }}
      {{- end }}
      avro_union_mode = {{ default "nullable" .value.union_mode | quote }}
      avro_field_separator = {{ default "" .value.union_field_separator | quote }}
      {{- if .value.fields }}
      avro_fields = {{ include "telegraf.toTomlArray" .value.fields }}
      {{- end }}
      {{- if .value.tags }}
      avro_tags = {{ include "telegraf.toTomlArray" .value.tags }}
      {{- end }}
      {{- else }}
    [[inputs.kafka_consumer.json_v2]]
      measurement_name_path = "measurement"
      [[inputs.kafka_consumer.json_v2.object]]

        path = "@this"
        timestamp_key = {{ .timestampField | quote }}
        timestamp_format = {{ default "unix" .value.timestamp_format | quote }}
        tags = {{ include "telegraf.toTomlArray" .value.tags }}
        excluded_keys = ["measurement"]
      {{- end }}
{{ end -}}

{{- define "configmap" -}}
{{- if .value.enabled }}
{{- include "telegraf.validateTopicDiscovery" . }}
{{- $topicDiscovery := default dict .value.topicDiscovery }}
{{- $discoveryEnabled := default false $topicDiscovery.enabled }}
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: sasquatch-telegraf-{{ .key }}
  labels:
    app.kubernetes.io/name: sasquatch-telegraf
    app.kubernetes.io/instance: sasquatch-telegraf-{{ .key }}
    app.kubernetes.io/part-of: sasquatch
data:
  telegraf.conf: |+
    [agent]
      metric_batch_size = {{ default 1000 .value.metric_batch_size }}
      metric_buffer_limit = {{ default 100000 .value.metric_buffer_limit }}
      collection_jitter = {{ default "0s" .value.collection_jitter | quote }}
      flush_interval = {{ default "10s" .value.flush_interval | quote }}
      flush_jitter = {{ default "0s" .value.flush_jitter | quote }}
      debug = {{ default false .value.debug }}
      omit_hostname = true
      skip_processors_after_aggregators = false
      logformat = "structured"


    {{- $database := .value.database }}
    {{- $timestampField := "private_efdStamp" }}
    {{- if hasKey .value "timestamp_field" }}
    {{- $timestampField = .value.timestamp_field }}
    {{- end }}
    {{- $compressionCodec := 3 }}
    {{- if hasKey .value "compression_codec" }}
    {{- $compressionCodec = .value.compression_codec }}
    {{- end }}
    {{- range .influxdbUrls }}
    [[outputs.influxdb]]
      namedrop = ["telegraf_*"]
      urls = [{{ . | quote }}]
      database = {{ $database | quote }}
      timeout = "15s"
      username = "${INFLUXDB_USER}"
      password = "${INFLUXDB_PASSWORD}"
    {{ end }}

    {{- range .influxdbUrls }}
    [[outputs.influxdb]]
      namepass = ["telegraf_*"]
      urls = [{{ . | quote }}]
      database = "telegraf"
      timeout = "15s"
      username = "${INFLUXDB_USER}"
      password = "${INFLUXDB_PASSWORD}"
    {{ end }}

    {{- $config := . }}
    {{- $consumers := list (dict
      "consumerGroup" (printf "telegraf-kafka-consumer-%s" .key)
      "offset" (default "oldest" .value.offset)
    ) }}
    {{- if .value.repair }}
    {{- $consumers = append $consumers (dict
      "consumerGroup" (printf "telegraf-kafka-consumer-%s-repairer" .key)
      "offset" "oldest"
    ) }}
    {{- end }}
    {{- if not $discoveryEnabled }}
    {{- range $consumer := $consumers }}
{{ include "telegraf.kafkaConsumer" (dict
  "value" $config.value
  "registryUrl" $config.registryUrl
  "kafkaVersion" $config.kafkaVersion
  "timestampField" $timestampField
  "compressionCodec" $compressionCodec
  "consumerGroup" $consumer.consumerGroup
  "offset" $consumer.offset
  "useTopics" false
) }}
    {{- end }}
    {{- end }}

    [[inputs.internal]]
      name_prefix = "telegraf_"
      collect_memstats = true
      tags = { instance = "{{ .key }}" }
  {{- if $discoveryEnabled }}
  kafka-consumer.conf.tmpl: |+
    {{- range $consumer := $consumers }}
{{ include "telegraf.kafkaConsumer" (dict
  "value" $config.value
  "registryUrl" $config.registryUrl
  "kafkaVersion" $config.kafkaVersion
  "timestampField" $timestampField
  "compressionCodec" $compressionCodec
  "consumerGroup" $consumer.consumerGroup
  "offset" $consumer.offset
  "useTopics" true
) }}
    {{- end }}
  include-prefixes.txt: |-
    {{- range $prefix := $topicDiscovery.includePrefixes }}
    {{ $prefix }}
    {{- end }}
  exclude-prefixes.txt: |-
    {{- range $prefix := (default list $topicDiscovery.excludePrefixes) }}
    {{ $prefix }}
    {{- end }}
  {{- end }}
{{- end }}
{{- end }}
