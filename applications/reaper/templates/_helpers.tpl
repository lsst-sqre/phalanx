{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "reaper.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "reaper.labels" -}}
helm.sh/chart: {{ include "reaper.chart" . }}
{{ include "reaper.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "reaper.selectorLabels" -}}
app.kubernetes.io/name: "reaper"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
