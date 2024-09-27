{{/* Define a helper to get the current timestamp */}}
{{- define "getCurrentTimestamp" -}}
{{- now | date "20060102150405" }}
{{- end -}}