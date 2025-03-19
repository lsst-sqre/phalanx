{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "mpsky.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mpsky.labels" -}}
helm.sh/chart: {{ include "mpsky.chart" . }}
{{ include "mpsky.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mpsky.selectorLabels" -}}
app.kubernetes.io/name: "mpsky"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
