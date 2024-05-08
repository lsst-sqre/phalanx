{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "butler-example-service.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "butler-example-service.labels" -}}
helm.sh/chart: {{ include "butler-example-service.chart" . }}
{{ include "butler-example-service.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "butler-example-service.selectorLabels" -}}
app.kubernetes.io/name: "butler-example-service"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
