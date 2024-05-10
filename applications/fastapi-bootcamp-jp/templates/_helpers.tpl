{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "fastapi-bootcamp-jp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "fastapi-bootcamp-jp.labels" -}}
helm.sh/chart: {{ include "fastapi-bootcamp-jp.chart" . }}
{{ include "fastapi-bootcamp-jp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "fastapi-bootcamp-jp.selectorLabels" -}}
app.kubernetes.io/name: "fastapi-bootcamp-jp"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
