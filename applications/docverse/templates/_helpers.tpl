{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "docverse.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "docverse.labels" -}}
helm.sh/chart: {{ include "docverse.chart" . }}
{{ include "docverse.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "docverse.selectorLabels" -}}
app.kubernetes.io/name: "docverse"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
