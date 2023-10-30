{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "butler.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "butler.labels" -}}
helm.sh/chart: {{ include "butler.chart" . }}
{{ include "butler.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "butler.selectorLabels" -}}
app.kubernetes.io/name: "butler"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
