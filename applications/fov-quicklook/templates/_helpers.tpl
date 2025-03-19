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
