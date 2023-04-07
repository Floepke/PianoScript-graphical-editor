import json

editor_settings_default = {"editor-x-zoom":35,"editor-y-percent":0.8}
SETTINGS = {}
try:
	with open('editor_settings.json', 'r') as f:
		if f:
			SETTINGS = json.load(f)
except:
	with open('editor_settings.json', 'w') as f:
		f.write(json.dumps(editor_settings_default, separators=(',', ':')))
		SETTINGS = editor_settings_default

print(SETTINGS)