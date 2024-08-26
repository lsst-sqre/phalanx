{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "obsenv-api.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "obsenv-api.labels" -}}
helm.sh/chart: {{ include "obsenv-api.chart" . }}
{{ include "obsenv-api.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "obsenv-api.selectorLabels" -}}
app.kubernetes.io/name: "obsenv-api"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
