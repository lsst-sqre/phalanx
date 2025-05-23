{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "google-cloud-observability.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "google-cloud-observability.labels" -}}
helm.sh/chart: {{ include "google-cloud-observability.chart" . }}
{{ include "google-cloud-observability.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "google-cloud-observability.selectorLabels" -}}
app.kubernetes.io/name: "google-cloud-observability"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}


{{/*
datasource-syncer container
*/}}
{{- define "google-cloud-observability.datasource-syncer-container" -}}
image: "{{ .Values.datasourceSyncer.image.repository}}:{{ .Values.datasourceSyncer.image.tag }}"
env:
  # Not in documentation, but here in code:
  # https://github.com/GoogleCloudPlatform/prometheus-engine/blob/e0d22812c5a449dd722de9802782bd01d806b352/cmd/datasource-syncer/main.go#L80
  - name: GRAFANA_SERVICE_ACCOUNT_TOKEN
    valueFrom:
      secretKeyRef:
        name: google-cloud-observability
        key: grafana-datasource-syncer-token
args:
  - "--datasource-uids={{ .Values.grafana.datasource.uid | required "grafana.datasource.uid must be filled in. It should be an existing, manually created, data source in Grafana." }}"
  - "--grafana-api-endpoint={{ .Values.grafana.url }}"
  - "--project-id={{ .Values.googleCloud.projectId | required "googleCloud.projectId must be set" }}"
{{- end }}


