{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "onepassword-connect.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "onepassword-connect.labels" -}}
helm.sh/chart: {{ include "onepassword-connect.chart" . }}
{{ include "onepassword-connect.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "onepassword-connect.selectorLabels" -}}
app.kubernetes.io/name: "onepassword-connect"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
