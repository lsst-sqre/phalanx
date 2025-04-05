{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ook.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ook.labels" -}}
helm.sh/chart: {{ include "ook.chart" . }}
{{ include "ook.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ook.selectorLabels" -}}
app.kubernetes.io/name: "ook"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Cloud SQL Auth Proxy sidecar container
*/}}
{{- define "ook.cloudsqlSidecar" -}}
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
Common environment variables
*/}}
{{- define "ook.envVars" -}}
# Writeable directory for concatenating certs. See "tmp" volume.
- name: "KAFKA_CERT_TEMP_DIR"
  value: "/tmp/kafka_certs"
- name: "KAFKA_SECURITY_PROTOCOL"
  value: "SSL"
# From KafkaAccess
- name: "KAFKA_BOOTSTRAP_SERVERS"
  valueFrom:
    secretKeyRef:
      name: "ook-kafka"
      key: "bootstrapServers"
- name: "KAFKA_CLUSTER_CA_PATH"
  value: "/etc/kafkacluster/ca.crt"
- name: "KAFKA_CLIENT_CERT_PATH"
  value: "/etc/kafkauser/user.crt"
- name: "KAFKA_CLIENT_KEY_PATH"
  value: "/etc/kafkauser/user.key"
# From Vault secrets
- name: "ALGOLIA_APP_ID"
  valueFrom:
    secretKeyRef:
      name: "ook"
      key: "ALGOLIA_APP_ID"
- name: "ALGOLIA_API_KEY"
  valueFrom:
    secretKeyRef:
      name: "ook"
      key: "ALGOLIA_API_KEY"
- name: "OOK_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "ook"
      key: "OOK_DATABASE_PASSWORD"
- name: "OOK_GITHUB_APP_ID"
  valueFrom:
    secretKeyRef:
      name: "ook"
      key: "OOK_GITHUB_APP_ID"
- name: "OOK_GITHUB_APP_PRIVATE_KEY"
  valueFrom:
    secretKeyRef:
      name: "ook"
      key: "OOK_GITHUB_APP_PRIVATE_KEY"
{{- end }}
