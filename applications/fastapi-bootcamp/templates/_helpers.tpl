{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "fastapi-bootcamp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "fastapi-bootcamp.labels" -}}
helm.sh/chart: {{ include "fastapi-bootcamp.chart" . }}
{{ include "fastapi-bootcamp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "fastapi-bootcamp.selectorLabels" -}}
app.kubernetes.io/name: "fastapi-bootcamp"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
