#!/bin/bash

# diShine Data-Safe USB — Setup Script
# Creates a virtual environment and installs all dependencies.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "--------------------------------------------------"
echo "   diShine Data-Safe USB — Setup"
echo "--------------------------------------------------"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Install it from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

source venv/bin/activate

# Upgrade pip
pip install --upgrade pip --quiet

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Download spaCy model for PII analysis
echo "Downloading spaCy NLP model (en_core_web_lg)..."
python3 -m spacy download en_core_web_lg --quiet

echo ""
echo "--------------------------------------------------"
echo "  Setup complete."
echo "  Run: ./Data_Safe.command"
echo "--------------------------------------------------"
