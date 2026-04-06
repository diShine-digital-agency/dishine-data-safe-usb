#!/bin/bash

# diShine Data-Safe USB - Setup Script
# This script sets up the virtual environment and installs all dependencies.

echo "--------------------------------------------------"
echo "   diShine Data-Safe USB - Initializing..."
echo "--------------------------------------------------"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment
echo "Creating Virtual Environment (venv)..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies (pandas, presidio, faker, rich)..."
pip install pandas presidio-analyzer presidio-anonymizer faker rich python-dotenv

# Download spaCy model for PII analysis
echo "Downloading spaCy NLP model (en_core_web_lg)..."
python3 -m spacy download en_core_web_lg

echo "--------------------------------------------------"
echo "Setup Complete! "
echo "To start, use: ./Data_Safe.command"
echo "--------------------------------------------------"
