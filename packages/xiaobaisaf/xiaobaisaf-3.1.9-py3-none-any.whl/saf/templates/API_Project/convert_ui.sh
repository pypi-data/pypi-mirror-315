#!/usr/bin/env bash

echo -e "\033]0;running...\007"

if [ -d "venv" ]; then
    if [-z "${OLD_VIRTUAL_PS1:-}"]; then
      . venv/bin/activate
    fi
else
    python3 -m venv venv
    . venv/bin/activate
fi

pip install -r requirements.txt --upgrade
python convert_ui.py
