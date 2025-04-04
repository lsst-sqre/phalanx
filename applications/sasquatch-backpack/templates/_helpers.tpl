{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "sasquatch-backpack.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "sasquatch-backpack.labels" -}}
helm.sh/chart: {{ include "sasquatch-backpack.chart" . }}
{{ include "sasquatch-backpack.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "sasquatch-backpack.selectorLabels" -}}
app.kubernetes.io/name: "sasquatch-backpack"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

