#!/bin/bash

# Check for Python 3.9.x installation
PYTHON_VERSION=$(python3 --version)
if [[ "$PYTHON_VERSION" =~ Python\ 3\.9 ]]; then
    echo "Python 3.9.x is installed."
else
    echo "Error: Python 3.9.x is not installed."
    exit 1
fi

# need to run the other commands here that are on the google docs.

# Check if requirements.txt exists in the current directory
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt does not exist in the current directory."
    exit 1
fi

# Optional: Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements from requirements.txt
echo "Installing requirements from requirements.txt..."
pip install -r requirements.txt

echo "Installation complete."
