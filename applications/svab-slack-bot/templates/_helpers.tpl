{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "svab-slack-bot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "svab-slack-bot.labels" -}}
helm.sh/chart: {{ include "svab-slack-bot.chart" . }}
{{ include "svab-slack-bot.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "svab-slack-bot.selectorLabels" -}}
app.kubernetes.io/name: "svab-slack-bot"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
