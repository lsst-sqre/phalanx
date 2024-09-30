{{/*
Convert a list to a TOML array of quoted string values
*/}}
{{- define "helpers.toTomlArray" -}}
{{- $items := list -}}
{{- range . -}}
{{- $items = (quote .) | append $items -}}
{{- end -}}
[ {{ join ", " $items }} ]
{{- end -}}
