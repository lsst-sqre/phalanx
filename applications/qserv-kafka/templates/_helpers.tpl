{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "qserv-kafka.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "qserv-kafka.labels" -}}
helm.sh/chart: {{ include "qserv-kafka.chart" . }}
{{ include "qserv-kafka.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "qserv-kafka.selectorLabels" -}}
app.kubernetes.io/name: "qserv-kafka"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Common environment variables
*/}}
{{- define "qserv-kafka.envVars" -}}
- name: "KAFKA_BOOTSTRAP_SERVERS"
  valueFrom:
    secretKeyRef:
      name: "qserv-kafka-access"
      key: "bootstrapServers"
- name: "KAFKA_CLIENT_CERT_PATH"
  value: "/etc/qserv-kafka/user.crt"
- name: "KAFKA_CLIENT_KEY_PATH"
  value: "/etc/qserv-kafka/user.key"
- name: "KAFKA_CLUSTER_CA_PATH"
  value: "/etc/qserv-kafka/ca.crt"
- name: "KAFKA_SECURITY_PROTOCOL"
  valueFrom:
    secretKeyRef:
      name: "qserv-kafka-access"
      key: "securityProtocol"
- name: "QSERV_KAFKA_GAFAELFAWR_TOKEN"
  valueFrom:
    secretKeyRef:
      name: "qserv-kafka-token"
      key: "token"
- name: "QSERV_KAFKA_QSERV_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "qserv-kafka"
      key: "qserv-password"
- name: "QSERV_KAFKA_REDIS_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "qserv-kafka"
      key: "redis-password"
{{- if .Values.config.qservRestUsername }}
- name: "QSERV_KAFKA_QSERV_REST_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "qserv-kafka"
      key: "qserv-password"
{{- end }}
{{- end }}
