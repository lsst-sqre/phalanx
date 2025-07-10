{{/* Shared environment configuration between scaled-job.yaml and_service_init.tpl */}}

{{/* initContainer definition that copies and chowns, and chmods the database
 auth files so that they are only readable by the container user.  Because of
 security checks in the code that uses it, this file must not be group or world readable.
*/}}
{{- define "prompt-keda.dbauth-initcontainer" -}}
- name: init-db-auth
  # Make a copy of the read-only secret that's owned by lsst
  # lsst account is created by main image with id 1000
  image: busybox
  imagePullPolicy: IfNotPresent
  command:
    [
    "sh",
    "-c",
    "cp -L /app/db-auth-mount/db-auth.yaml /app/dbauth/ && chown 1000:1000 /app/dbauth/db-auth.yaml && chmod u=r,go-rwx /app/dbauth/db-auth.yaml",
    ]
  volumeMounts:
    - mountPath: /app/db-auth-mount
      name: db-auth-mount
      readOnly: true
    - mountPath: /app/dbauth
      name: db-auth-credentials-file
{{- end }}

{{/* volumes containing credential files used by PP and Science Pipelines */}}
{{- define "prompt-keda.credentials-volumes" -}}
- name: db-auth-mount
  # Temporary mount for db-auth.yaml; cannot be read directly because it's owned by root
  secret:
    secretName: {{ template "prompt-keda.fullname" . }}-secret
    defaultMode: 256
    items:
      - key: db-auth_file
        path: db-auth.yaml
- name: db-auth-credentials-file
  emptyDir:
    sizeLimit: 10Ki # Just a text file!
{{- if .Values.s3.cred_file_auth }}
- name: s3-credentials-file
  secret:
    secretName: {{ template "prompt-keda.fullname" . }}-secret
    items:
      - key: s3_credentials_file
        path: credentials
{{- end }}
{{- end }}

{{/* volumeMounts containing credential files used by PP and Science Pipelines */}}
{{- define "prompt-keda.credentials-volumeMounts" -}}
- mountPath: /app/lsst-credentials
  name: db-auth-credentials-file
  readOnly: true
{{- if .Values.s3.cred_file_auth }}
- mountPath: /app/s3/
  name: s3-credentials-file
{{- end }}
{{- end }}

{{/* Environment variables used to configure Science Pipelines credentials */}}
{{- define "prompt-keda.db-auth-env" -}}
- name: LSST_DB_AUTH
  value: /app/lsst-credentials/db-auth.yaml
{{- end }}

{{/* Environment variables used to configure S3
     Don't know why the first if needs an extra whitespace chomp.
 */}}
{{- define "prompt-keda.s3-env" -}}
{{- if .Values.s3.cred_file_auth -}}
- name: AWS_SHARED_CREDENTIALS_FILE
  value: /app/s3/credentials
{{- end }}
- name: S3_ENDPOINT_URL
  value: {{ .Values.s3.endpointUrl }}
{{- if .Values.s3.auth_env }}
- name: AWS_ACCESS_KEY_ID
  valueFrom:
    secretKeyRef:
      name: {{ template "prompt-keda.fullname" . }}-secret
      key: s3_access_key
- name: AWS_SECRET_ACCESS_KEY
  valueFrom:
    secretKeyRef:
      name: {{ template "prompt-keda.fullname" . }}-secret
      key: s3_secret_key
{{- end }}
{{- with .Values.s3.aws_profile }}
  {{- if not $.Values.s3.cred_file_auth }}
    {{- fail "When s3.aws_profile is set, s3.cred_file_auth must be true." }}
  {{- end }}
- name: AWS_PROFILE
  value: {{ . }}
{{- end }}
{{- with .Values.s3.checksum }}
- name: AWS_REQUEST_CHECKSUM_CALCULATION
  value: {{ . }}
{{- end }}
{{- end }}
