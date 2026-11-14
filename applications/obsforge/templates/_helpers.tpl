{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "obsforge.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "obsforge.labels" -}}
helm.sh/chart: {{ include "obsforge.chart" . }}
{{ include "obsforge.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "obsforge.selectorLabels" -}}
app.kubernetes.io/name: "obsforge"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Validate component configuration
*/}}
{{- define "obsforge.validateValues" -}}
{{- if and (or .Values.api.enabled .Values.worker.enabled) (not .Values.redis.enabled) -}}
{{- fail "redis.enabled must be true when api.enabled or worker.enabled is true" -}}
{{- end -}}
{{- end }}

{{/*
API environment variables from secrets
*/}}
{{- define "obsforge.apiEnvVars" -}}
- name: "OBSFORGE_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "database-password"
- name: "OBSFORGE_ARQ_QUEUE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "redis-password"
{{- if .Values.config.slackAlerts }}
- name: "OBSFORGE_SLACK_WEBHOOK"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "slack-webhook"
{{- end }}
{{- end }}

{{/*
Worker environment variables from secrets
*/}}
{{- define "obsforge.workerEnvVars" -}}
- name: "OBSFORGE_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "database-password"
- name: "OBSFORGE_ARQ_QUEUE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "redis-password"
- name: "OBSFORGE_BUTLER_ACCESS_TOKEN"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "butler-access-token"
{{- end }}

{{/*
Stream worker environment variables from secrets
*/}}
{{- define "obsforge.streamEnvVars" -}}
- name: "OBSFORGE_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "database-password"
- name: "OBSFORGE_KAFKA_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "kafka-password"
- name: "OBSFORGE_SCHEMA_REGISTRY_TOKEN"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "schema-registry-token"
{{- end }}

{{/*
Schema update environment variables from secrets
*/}}
{{- define "obsforge.schemaEnvVars" -}}
- name: "OBSFORGE_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "obsforge"
      key: "database-password"
{{- end }}
