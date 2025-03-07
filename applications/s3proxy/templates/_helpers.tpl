{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "s3proxy.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "s3proxy.labels" -}}
helm.sh/chart: {{ include "s3proxy.chart" . }}
{{ include "s3proxy.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "s3proxy.selectorLabels" -}}
app.kubernetes.io/name: "s3proxy"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
