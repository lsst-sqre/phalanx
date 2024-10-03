{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "templatebot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "templatebot.labels" -}}
helm.sh/chart: {{ include "templatebot.chart" . }}
{{ include "templatebot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "templatebot.selectorLabels" -}}
app.kubernetes.io/name: "templatebot"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
