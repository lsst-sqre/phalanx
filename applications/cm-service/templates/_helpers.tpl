{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "cm-service.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "cm-service.labels" -}}
helm.sh/chart: {{ include "cm-service.chart" . }}
{{ include "cm-service.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "cm-service.selectorLabels" -}}
app.kubernetes.io/name: "cm-service"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
