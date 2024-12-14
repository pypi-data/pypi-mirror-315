title running...

if not exist venv ( python -m venv venv )
if defined _OLD_VIRTUAL_PROMPT (
	pip install -r requirements.txt --upgrade & python convert_ui.py
) else (
	venv\Scripts\activate.bat & pip install -r requirements.txt --upgrade & python convert_ui.py
)
