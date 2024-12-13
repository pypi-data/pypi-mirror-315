title running...

if not exist venv ( python -m venv venv )

if not defined _OLD_VIRTUAL_PROMPT ( venv\Scripts\activate.bat )

pip install -r requirements.txt --upgrade
python convert_ui.py
