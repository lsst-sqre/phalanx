{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "onepassword-connect-dev.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "onepassword-connect-dev.labels" -}}
helm.sh/chart: {{ include "onepassword-connect-dev.chart" . }}
{{ include "onepassword-connect-dev.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "onepassword-connect-dev.selectorLabels" -}}
app.kubernetes.io/name: "onepassword-connect-dev"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
