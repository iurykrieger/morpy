#!/bin/bash

# Activates 'morpy' venv
echo "# Activating morpy virtual envroinment..."
source activate morpy

# Run application
echo "# Running application..."
python -m compileall . &>/dev/null
python run.py