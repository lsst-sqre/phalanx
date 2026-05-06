{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "influxdb-migration.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "influxdb-migration.labels" -}}
helm.sh/chart: {{ include "influxdb-migration.chart" . }}
{{ include "influxdb-migration.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "influxdb-migration.selectorLabels" -}}
app.kubernetes.io/name: "influxdb-migration"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
