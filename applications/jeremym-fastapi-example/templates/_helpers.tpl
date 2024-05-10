{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "jeremym-fastapi-example.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "jeremym-fastapi-example.labels" -}}
helm.sh/chart: {{ include "jeremym-fastapi-example.chart" . }}
{{ include "jeremym-fastapi-example.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "jeremym-fastapi-example.selectorLabels" -}}
app.kubernetes.io/name: "jeremym-fastapi-example"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
