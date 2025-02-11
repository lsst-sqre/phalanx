{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "prompt-processing-redis.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "prompt-processing-redis.labels" -}}
helm.sh/chart: {{ include "prompt-processing-redis.chart" . }}
{{ include "prompt-processing-redis.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "prompt-processing-redis.selectorLabels" -}}
app.kubernetes.io/name: "prompt-processing-redis"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
