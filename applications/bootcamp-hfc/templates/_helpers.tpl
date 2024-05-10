{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "bootcamp-hfc.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "bootcamp-hfc.labels" -}}
helm.sh/chart: {{ include "bootcamp-hfc.chart" . }}
{{ include "bootcamp-hfc.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "bootcamp-hfc.selectorLabels" -}}
app.kubernetes.io/name: "bootcamp-hfc"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
