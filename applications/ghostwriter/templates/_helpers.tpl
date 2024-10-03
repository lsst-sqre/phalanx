{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ghostwriter.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ghostwriter.labels" -}}
helm.sh/chart: {{ include "ghostwriter.chart" . }}
{{ include "ghostwriter.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ghostwriter.selectorLabels" -}}
app.kubernetes.io/name: "ghostwriter"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
