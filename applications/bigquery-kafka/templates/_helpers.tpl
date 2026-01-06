{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "bigquery-kafka.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "bigquery-kafka.labels" -}}
helm.sh/chart: {{ include "bigquery-kafka.chart" . }}
{{ include "bigquery-kafka.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "bigquery-kafka.selectorLabels" -}}
app.kubernetes.io/name: "bigquery-kafka"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Common environment variables
*/}}
{{- define "bigquery-kafka.envVars" -}}
- name: "KAFKA_BOOTSTRAP_SERVERS"
  valueFrom:
    secretKeyRef:
      name: "bigquery-kafka-access"
      key: "bootstrapServers"
- name: "KAFKA_CLUSTER_CA_PATH"
  value: "/etc/bigquery-kafka/ca.crt"
- name: "KAFKA_CLIENT_CERT_PATH"
  value: "/etc/bigquery-kafka/user.crt"
- name: "KAFKA_CLIENT_KEY_PATH"
  value: "/etc/bigquery-kafka/user.key"
- name: "KAFKA_SECURITY_PROTOCOL"
  valueFrom:
    secretKeyRef:
      name: "bigquery-kafka-access"
      key: "securityProtocol"
- name: "QSERV_KAFKA_GAFAELFAWR_TOKEN"
  valueFrom:
    secretKeyRef:
      name: "bigquery-kafka-token"
      key: "token"
{{- if eq .Values.config.enabledBackend "QSERV" }}
- name: "QSERV_KAFKA_QSERV_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "bigquery-kafka"
      key: "qserv-password"
{{- end }}
- name: "QSERV_KAFKA_REDIS_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "bigquery-kafka"
      key: "redis-password"
{{- if .Values.config.qservRestUsername }}
- name: "QSERV_KAFKA_QSERV_REST_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "bigquery-kafka"
      key: "qserv-password"
{{- end }}
{{- if .Values.config.slack.enabled }}
- name: "QSERV_KAFKA_SLACK_WEBHOOK"
  valueFrom:
    secretKeyRef:
      name: "bigquery-kafka"
      key: "slack-webhook"
{{- end }}
{{- if .Values.config.sentry.enabled }}
- name: "SENTRY_DSN"
  valueFrom:
    secretKeyRef:
      name: "bigquery-kafka"
      key: "sentry-dsn"
- name: "SENTRY_ENVIRONMENT"
  value: {{ .Values.global.environmentName | quote }}
- name: "SENTRY_TRACES_SAMPLE_RATE"
  value: {{ .Values.config.sentry.tracesSampleRate | quote }}
{{- end }}
{{- end }}
