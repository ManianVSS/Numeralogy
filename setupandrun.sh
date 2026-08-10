#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

if [[ -x ".venv/bin/python" ]]; then
    echo "Virtual environment already exists. Skipping creation and package installation."
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created."
    echo "Installing requirements..."
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    deactivate
fi

echo "Activating virtual environment..."
source .venv/bin/activate
echo "Starting the Numeralogy application..."
python numerology_pyqt.py
