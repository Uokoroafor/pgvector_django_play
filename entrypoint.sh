#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status.

# echo "Checking for .env file..."
# python generate_env.py

# Define a marker file path
MARKER_FILE="Markerfile"

# Check if the marker file exists
if [ ! -f "$MARKER_FILE" ]; then
    echo "Running first-time init script..."
    bash ./get_texts.sh
    python load_texts.py
    
    python manage.py migrate --noinput
    echo "First-time setup complete."

    # Create the marker file
    touch "$MARKER_FILE"
else
    echo "Initialization script already ran. Skipping..."
fi

echo "Starting App..."
python manage.py runserver 0.0.0.0:8000