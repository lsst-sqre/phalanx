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
{{- if .Values.config.credentialKeyRotation }}
- name: "DOCVERSE_CREDENTIAL_ENCRYPTION_KEY_RETIRED"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "DOCVERSE_CREDENTIAL_ENCRYPTION_KEY_RETIRED"
{{- end }}
- name: "DOCVERSE_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "DOCVERSE_DATABASE_PASSWORD"
{{- if .Values.config.githubAppId }}
- name: "DOCVERSE_GITHUB_APP_PRIVATE_KEY"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "DOCVERSE_GITHUB_APP_PRIVATE_KEY"
- name: "DOCVERSE_GITHUB_WEBHOOK_SECRET"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "DOCVERSE_GITHUB_WEBHOOK_SECRET"
{{- end }}
{{- if .Values.config.slackAlerts }}
- name: "DOCVERSE_SLACK_WEBHOOK"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "slack-webhook"
{{- end }}
{{- if .Values.config.sentry.enabled }}
- name: "SENTRY_DSN"
  valueFrom:
    secretKeyRef:
      name: "docverse"
      key: "SENTRY_DSN"
- name: "SENTRY_ENVIRONMENT"
  value: {{ .Values.global.environmentName | quote }}
- name: "SENTRY_TRACES_SAMPLE_RATE"
  value: {{ .Values.config.sentry.tracesSampleRate | quote }}
{{- end }}
{{- end }}

{{/*
Kafka connection environment variables for application-metrics publishing,
sourced from the access-operator-minted docverse-kafka secret plus the static
mount paths. Included only by the long-running metric-publishing pods (the API
and the three worker pools) — deliberately NOT part of docverse.envVars, so the
PreSync schema-update job never references the docverse-kafka secret (which the
access operator only mints during the main sync wave). Self-gated on
config.metrics.enabled.
*/}}
{{- define "docverse.kafkaEnvVars" -}}
{{- if .Values.config.metrics.enabled }}
- name: "KAFKA_BOOTSTRAP_SERVERS"
  valueFrom:
    secretKeyRef:
      name: "docverse-kafka"
      key: "bootstrapServers"
- name: "KAFKA_SECURITY_PROTOCOL"
  valueFrom:
    secretKeyRef:
      name: "docverse-kafka"
      key: "securityProtocol"
- name: "KAFKA_CLIENT_CERT_PATH"
  value: "/etc/docverse-kafka/user.crt"
- name: "KAFKA_CLIENT_KEY_PATH"
  value: "/etc/docverse-kafka/user.key"
- name: "KAFKA_CLUSTER_CA_PATH"
  value: "/etc/docverse-kafka/ca.crt"
{{- end }}
{{- end }}

{{/*
Volume mounts for the Kafka client certificate material minted by the Strimzi
access operator into the docverse-kafka secret. Included by every pod that
publishes application metrics when config.metrics.enabled is true.
*/}}
{{- define "docverse.kafkaVolumeMounts" -}}
- name: "kafka"
  mountPath: "/etc/docverse-kafka/ca.crt"
  readOnly: true
  subPath: "ssl.truststore.crt"
- name: "kafka"
  mountPath: "/etc/docverse-kafka/user.crt"
  readOnly: true
  subPath: "ssl.keystore.crt"
- name: "kafka"
  mountPath: "/etc/docverse-kafka/user.key"
  readOnly: true
  subPath: "ssl.keystore.key"
{{- end }}

{{/*
The Kafka client certificate volume sourced from the docverse-kafka secret.
Included by every pod that publishes application metrics when
config.metrics.enabled is true.
*/}}
{{- define "docverse.kafkaVolume" -}}
- name: "kafka"
  secret:
    secretName: "docverse-kafka"
{{- end }}
