{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "skyviewer.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "skyviewer.labels" -}}
helm.sh/chart: {{ include "skyviewer.chart" . }}
{{ include "skyviewer.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "skyviewer.selectorLabels" -}}
app.kubernetes.io/name: "skyviewer"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
