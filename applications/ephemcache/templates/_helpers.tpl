{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ephemcache.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ephemcache.labels" -}}
helm.sh/chart: {{ include "ephemcache.chart" . }}
{{ include "ephemcache.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ephemcache.selectorLabels" -}}
app.kubernetes.io/name: "ephemcache"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
