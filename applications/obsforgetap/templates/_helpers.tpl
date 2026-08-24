{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "obsforgetap.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "obsforgetap.labels" -}}
helm.sh/chart: {{ include "obsforgetap.chart" . }}
{{ include "obsforgetap.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "obsforgetap.selectorLabels" -}}
app.kubernetes.io/name: "obsforgetap"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
