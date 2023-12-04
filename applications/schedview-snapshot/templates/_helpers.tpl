{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "schedview-snapshot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "schedview-snapshot.labels" -}}
helm.sh/chart: {{ include "schedview-snapshot.chart" . }}
{{ include "schedview-snapshot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "schedview-snapshot.selectorLabels" -}}
app.kubernetes.io/name: "schedview-snapshot"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
