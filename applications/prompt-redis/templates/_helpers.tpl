{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "prompt-redis.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "prompt-redis.labels" -}}
helm.sh/chart: {{ include "prompt-redis.chart" . }}
{{ include "prompt-redis.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "prompt-redis.selectorLabels" -}}
app.kubernetes.io/name: "prompt-redis"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
