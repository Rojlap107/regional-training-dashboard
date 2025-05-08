#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d "dashboard_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv dashboard_env
fi

# Activate the virtual environment
source dashboard_env/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run the dashboard
echo "Starting the dashboard. Open http://127.0.0.1:8050/ in your web browser."
python dashboard.py