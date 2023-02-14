{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "hips.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "hips.labels" -}}
helm.sh/chart: {{ include "hips.chart" . }}
{{ include "hips.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "hips.selectorLabels" -}}
app.kubernetes.io/name: "hips"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
