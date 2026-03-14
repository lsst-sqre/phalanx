{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "herald.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "herald.labels" -}}
helm.sh/chart: {{ include "herald.chart" . }}
{{ include "herald.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "herald.selectorLabels" -}}
app.kubernetes.io/name: "herald"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
