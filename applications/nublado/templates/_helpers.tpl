{{/* vim: set filetype=mustache: */}}
{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "nublado.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "nublado.labels" -}}
helm.sh/chart: {{ include "nublado.chart" . }}
{{ include "nublado.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "nublado.selectorLabels" -}}
app.kubernetes.io/name: "nublado"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
