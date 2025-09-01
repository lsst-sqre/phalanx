{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "fov-quicklook.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "fov-quicklook.labels" -}}
helm.sh/chart: {{ include "fov-quicklook.chart" . }}
{{ include "fov-quicklook.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "fov-quicklook.selectorLabels" -}}
app.kubernetes.io/name: "fov-quicklook"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
