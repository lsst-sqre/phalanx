{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "eups-distributor.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "eups-distributor.labels" -}}
helm.sh/chart: {{ include "eups-distributor.chart" . }}
{{ include "eups-distributor.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "eups-distributor.selectorLabels" -}}
app.kubernetes.io/name: "eups-distributor"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
