{{- define "fov-quicklook.env.s3_tile" -}}
- name: QUICKLOOK_s3_tile
  value: {{ .Values.s3_tile | toJson | quote }}
- name: QUICKLOOK_s3_tile__access_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook
      key: s3_repository_access_key
- name: QUICKLOOK_s3_tile__secret_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook
      key: s3_repository_secret_key
{{- end }}

{{- define "fov-quicklook.env.db" -}}
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: fov-quicklook
      key: db_password
- name: QUICKLOOK_db_url
  value: postgresql://quicklook:$(DB_PASSWORD)@fov-quicklook-db:5432/quicklook
{{- end }}

{{- define "fov-quicklook.env.log-level" -}}
- name: QUICKLOOK_log_level
  value: {{ .Values.log_level | quote }}
{{- end }}


{{- define "quicklook.ingress.spec" -}}
rules:
  - host: {{ .Values.global.host | quote }}
    http:
      paths:
        - path: {{ .Values.config.pathPrefix }}
          pathType: Prefix
          backend:
            service:
              name: fov-quicklook-frontend
              port:
                number: 9500
{{- end -}}

{{- define "fov-quicklook.butler-settings.env" -}}
{{- range .Values.butler_settings.envs }}
- name: {{ .name }}
  value: {{ .value | quote }}
{{- end }}
{{- end }}
