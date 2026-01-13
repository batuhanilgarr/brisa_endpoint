#!/bin/bash
# Brisa API Başlatma Scripti

cd /home/bitiz/Desktop/brisa_endpoint

# Virtual environment varsa kullan, yoksa sistem Python'unu kullan
if [ -f "venv/bin/python" ]; then
    exec venv/bin/python api_server.py
elif [ -f "venv/bin/python3" ]; then
    exec venv/bin/python3 api_server.py
elif command -v python3 &> /dev/null; then
    exec python3 api_server.py
else
    exec python api_server.py
fi
