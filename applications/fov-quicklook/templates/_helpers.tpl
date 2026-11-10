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
- name: QUICKLOOK_s3_tile_key_prefix
  value: {{ .Values.config.s3_tile_path_prefix | quote }}
- name: QUICKLOOK_max_object_storage_usage
  value: {{ printf "%.0f" .Values.config.max_object_storage_usage | quote }}
{{- end }}

{{- define "fov-quicklook.env.cache" -}}
- name: QUICKLOOK_tile_cache_schema_version
  value: {{ .Values.config.tile_cache_schema_version | quote }}
{{- end }}

{{- define "fov-quicklook.env.db" -}}
- name: DB_NAME
  valueFrom:
    secretKeyRef:
      name: fov-quicklook-db
      key: db-name
- name: DB_HOST
  valueFrom:
    secretKeyRef:
      name: fov-quicklook-db
      key: db-url
- name: DB_USER
  valueFrom:
    secretKeyRef:
      name: fov-quicklook-db
      key: db-user
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: fov-quicklook-db
      key: password
- name: QUICKLOOK_db_url
  value: postgresql+asyncpg://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):5432/$(DB_NAME)
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

{{- define "fov-quicklook.env.ccd_data_types" -}}
{{- if .Values.ccd_data_types }}
- name: QUICKLOOK_ccd_data_types
  value: {{ .Values.ccd_data_types | toJson | quote }}
{{- end }}
{{- end }}
