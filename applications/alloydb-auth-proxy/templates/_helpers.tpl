{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "alloydb-auth-proxy.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "alloydb-auth-proxy.labels" -}}
helm.sh/chart: {{ include "alloydb-auth-proxy.chart" . }}
{{ include "alloydb-auth-proxy.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "alloydb-auth-proxy.selectorLabels" -}}
app.kubernetes.io/name: "alloydb-auth-proxy"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
