{{- define "configmap" -}}
{{- if .value.enabled }}
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

    [[outputs.influxdb]]
      namedrop = ["telegraf_*"]
      urls = [
        {{ .influxdbUrl | quote }}
      ]
      database = {{ .value.database | quote }}
      username = "${INFLUXDB_USER}"
      password = "${INFLUXDB_PASSWORD}"

    [[outputs.influxdb]]
      namepass = ["telegraf_*"]
      urls = [
        {{ .influxdbUrl | quote }}
      ]
      database = "telegraf"
      username = "${INFLUXDB_USER}"
      password = "${INFLUXDB_PASSWORD}"

    [[inputs.kafka_consumer]]
      brokers = [
        "sasquatch-kafka-brokers.sasquatch:9092"
      ]
      consumer_group = "telegraf-kafka-consumer-{{ .key }}"
      sasl_mechanism = "SCRAM-SHA-512"
      sasl_password = "$TELEGRAF_PASSWORD"
      sasl_username = "telegraf"
      data_format = "avro"
      avro_schema_registry = "http://sasquatch-schema-registry.sasquatch:8081"
      avro_timestamp = {{ default "private_efdStamp" .value.timestamp_field | quote }}
      avro_timestamp_format = {{ default "unix" .value.timestamp_format | quote }}
      avro_union_mode = {{ default "nullable" .value.union_mode | quote }}
      avro_field_separator = {{ default "" .value.union_field_separator | quote }}
      {{- if .value.fields }}
      avro_fields = {{ .value.fields }}
      {{- end }}
      {{- if .value.tags }}
      avro_tags = {{ .value.tags }}
      {{- end }}
      topic_regexps = {{ .value.topicRegexps }}
      offset = {{ default "oldest" .value.offset | quote }}
      precision = {{ default "1us" .value.precision | quote }}
      max_processing_time = {{ default "5s" .value.max_processing_time | quote }}
      consumer_fetch_default = {{ default "20MB" .value.consumer_fetch_default | quote }}
      max_undelivered_messages = {{ default 10000 .value.max_undelivered_messages }}
      compression_codec = {{ default 3 .value.compression_codec }}

    {{- if .value.repair }}
    [[inputs.kafka_consumer]]
      brokers = [
        "sasquatch-kafka-brokers.sasquatch:9092"
      ]
      consumer_group = "telegraf-kafka-consumer-{{ .key }}-repairer"
      sasl_mechanism = "SCRAM-SHA-512"
      sasl_password = "$TELEGRAF_PASSWORD"
      sasl_username = "telegraf"
      data_format = "avro"
      avro_schema_registry = "http://sasquatch-schema-registry.sasquatch:8081"
      avro_timestamp = {{ default "private_efdStamp" .value.timestamp_field | quote }}
      avro_timestamp_format = {{ default "unix" .value.timestamp_format | quote }}
      avro_union_mode = {{ default "nullable" .value.union_mode | quote }}
      avro_field_separator = {{ default "" .value.union_field_separator | quote }}
      {{- if .value.fields }}
      avro_fields = {{ .value.fields }}
      {{- end }}
      {{- if .value.tags }}
      avro_tags = {{ .value.tags }}
      {{- end }}
      topic_regexps = {{ .value.topicRegexps }}
      offset = "oldest"
      precision = {{ default "1us" .value.precision | quote }}
      max_processing_time = {{ default "5s" .value.max_processing_time | quote }}
      consumer_fetch_default = {{ default "20MB" .value.consumer_fetch_default | quote }}
      max_undelivered_messages = {{ default 10000 .value.max_undelivered_messages }}
      compression_codec = {{ default 3 .value.compression_codec }}
    {{- end }}

    [[inputs.internal]]
      name_prefix = "telegraf_"
      collect_memstats = true
      tags = { instance = "{{ .key }}" }
{{- end }}
{{- end }}
