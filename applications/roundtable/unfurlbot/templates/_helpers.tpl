{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "unfurlbot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "unfurlbot.labels" -}}
helm.sh/chart: {{ include "unfurlbot.chart" . }}
{{ include "unfurlbot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "unfurlbot.selectorLabels" -}}
app.kubernetes.io/name: "unfurlbot"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
