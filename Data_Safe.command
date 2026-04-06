#!/bin/bash
# --------------------------------------------------
# diShine Data-Safe USB — Quick Launch
# --------------------------------------------------

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    bash setup.sh
fi

source venv/bin/activate
python3 Data_Safe.py "$@"

read -p "Press Enter to exit..."
