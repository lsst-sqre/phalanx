{{/* vim: set filetype=mustache: */}}
{{- define "enabledServicesYamlList" }}
{{- range $app, $enabled := .Values.applications }}
  {{- if $enabled }}
- {{ $app | quote }}
  {{- end }}
{{- end }}
{{- end -}}
