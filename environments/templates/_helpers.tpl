{{/* vim: set filetype=mustache: */}}
{{- define "enabledServices" -}}
  {{- range $app, $enabled := .Values.applications }}
    {{- if $enabled }}@{{ $app }}{{ end }}
  {{- end }}
{{- end }}
