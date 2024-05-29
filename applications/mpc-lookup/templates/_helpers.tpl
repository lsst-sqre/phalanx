{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "mpc-lookup.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mpc-lookup.labels" -}}
helm.sh/chart: {{ include "mpc-lookup.chart" . }}
{{ include "mpc-lookup.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mpc-lookup.selectorLabels" -}}
app.kubernetes.io/name: "mpc-lookup"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
