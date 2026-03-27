{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "docverse.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "docverse.labels" -}}
helm.sh/chart: {{ include "docverse.chart" . }}
{{ include "docverse.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "docverse.selectorLabels" -}}
app.kubernetes.io/name: "docverse"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Cloud SQL Auth Proxy sidecar container
*/}}
{{- define "docverse.cloudsqlSidecar" -}}
- name: "cloud-sql-proxy"
  command:
    - "/cloud_sql_proxy"
    - "-ip_address_types=PRIVATE"
    - "-log_debug_stdout=true"
    - "-structured_logs=true"
    - "-instances={{ required "cloudsql.instanceConnectionName must be specified" .Values.cloudsql.instanceConnectionName }}=tcp:5432"
  image: "{{ .Values.cloudsql.image.repository }}:{{ .Values.cloudsql.image.tag }}"
  imagePullPolicy: {{ .Values.cloudsql.image.pullPolicy | quote }}
  {{- with .Values.cloudsql.resources }}
  resources:
    {{- toYaml . | nindent 12 }}
  {{- end }}
  restartPolicy: "Always"
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - "all"
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 65532
    runAsGroup: 65532
{{- end }}

{{/*
Secret environment variables shared across all Docverse pods.
*/}}
{{- define "docverse.envVars" -}}
- name: "DOCVERSE_CREDENTIAL_ENCRYPTION_KEY"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "DOCVERSE_CREDENTIAL_ENCRYPTION_KEY"
- name: "DOCVERSE_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "DOCVERSE_DATABASE_PASSWORD"
{{- if .Values.config.slackAlerts }}
- name: "DOCVERSE_SLACK_WEBHOOK"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "slack-webhook"
{{- end }}
{{- end }}
