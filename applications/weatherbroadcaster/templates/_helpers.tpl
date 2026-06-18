{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "weatherbroadcaster.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "weatherbroadcaster.labels" -}}
helm.sh/chart: {{ include "weatherbroadcaster.chart" . }}
{{ include "weatherbroadcaster.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "weatherbroadcaster.selectorLabels" -}}
app.kubernetes.io/name: "weatherbroadcaster"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
