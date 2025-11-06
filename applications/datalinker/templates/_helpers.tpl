{{/* vim: set filetype=mustache: */}}
{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "datalinker.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "datalinker.labels" -}}
helm.sh/chart: {{ include "datalinker.chart" . }}
{{ include "datalinker.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "datalinker.selectorLabels" -}}
app.kubernetes.io/name: "datalinker"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
