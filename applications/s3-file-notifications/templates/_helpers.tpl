{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "s3-file-notifications.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "s3-file-notifications.labels" -}}
helm.sh/chart: {{ include "s3-file-notifications.chart" . }}
{{ include "s3-file-notifications.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "s3-file-notifications.selectorLabels" -}}
app.kubernetes.io/name: "s3-file-notifications"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
