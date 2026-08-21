{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "sia.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "sia.labels" -}}
helm.sh/chart: {{ include "sia.chart" . }}
{{ include "sia.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "sia.selectorLabels" -}}
app.kubernetes.io/name: "sia"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
