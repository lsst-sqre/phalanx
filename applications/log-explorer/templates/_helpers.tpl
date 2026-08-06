{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "log-explorer.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "log-explorer.labels" -}}
helm.sh/chart: {{ include "log-explorer.chart" . }}
{{ include "log-explorer.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "log-explorer.selectorLabels" -}}
app.kubernetes.io/name: "log-explorer"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
