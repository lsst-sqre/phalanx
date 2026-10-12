{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "weathernbeats.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "weathernbeats.labels" -}}
helm.sh/chart: {{ include "weathernbeats.chart" . }}
{{ include "weathernbeats.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "weathernbeats.selectorLabels" -}}
app.kubernetes.io/name: "weathernbeats"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
