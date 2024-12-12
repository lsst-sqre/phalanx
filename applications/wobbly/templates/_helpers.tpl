{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "wobbly.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "wobbly.labels" -}}
helm.sh/chart: {{ include "wobbly.chart" . }}
{{ include "wobbly.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "wobbly.selectorLabels" -}}
app.kubernetes.io/name: "wobbly"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
