{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "gai-helpers.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "gai-helpers.labels" -}}
helm.sh/chart: {{ include "gai-helpers.chart" . }}
{{ include "gai-helpers.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "gai-helpers.selectorLabels" -}}
app.kubernetes.io/name: "gai-helpers"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
