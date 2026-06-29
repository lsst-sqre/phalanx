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
Common environment variables from secrets
*/}}
{{- define "obsforge.envVars" -}}
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
