{{/* vim: set filetype=mustache: */}}
{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "vo-cutouts.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "vo-cutouts.labels" -}}
helm.sh/chart: {{ include "vo-cutouts.chart" . }}
{{ include "vo-cutouts.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "vo-cutouts.selectorLabels" -}}
app.kubernetes.io/name: "vo-cutouts"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
