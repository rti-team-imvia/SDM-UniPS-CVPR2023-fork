#!/bin/bash

CURRENT_DIR=$(pwd)  # Get the current working directory

# A bash script to create a virtual environment in the cluster and install necessary packages.

######################
# VIRTUAL ENVIRONMENT
######################
# Check if the .venv directory exists
if [ -d ".venv" ]; then
    echo "Virtual environment '.venv' already exists."
else
    # Load the Python module
    echo "Loading Python 3.11 Anaconda module..."
    module load python/3.11/anaconda/2024.02

    # Create a virtual environment in the .venv directory
    echo "Creating virtual environment in '.venv'..."
    python -m venv .venv

    # Check if the virtual environment was created successfully
    if [ -d ".venv" ]; then
        echo "Virtual environment '.venv' created successfully."
    else
        echo "Failed to create virtual environment."
        exit 1
    fi
fi

######################
# ACTIVATE VIRTUAL ENVIRONMENT
######################
echo "Activating the virtual environment..."
source .venv/bin/activate

# Dynamically add the virtual environment's bin directory to PATH
echo "Adding .venv/bin directory to PATH..."
export PATH="$CURRENT_DIR/.venv/bin:$PATH"

######################
# UPGRADE PIP
######################
echo "Upgrading pip..."
python -m pip install --upgrade pip || { echo "Failed to upgrade pip"; exit 1; }

######################
# INSTALL NECESSARY PACKAGES
######################
# Install necessary packages with error checking
echo "Installing necessary packages..."

# List of packages to install
PACKAGES=(
    "torch torchvision --index-url https://download.pytorch.org/whl/cu118"
    "opencv-python-headless"
    "einops"
    "imageio"
)

# Loop through the packages array and install each one
for package in "${PACKAGES[@]}"; do
    echo "Installing $package..."
    pip install $package || { echo "Failed to install $package"; exit 1; }
done

echo "All packages installed successfully."

######################
# FINAL CONFIRMATION
######################
echo "Setup completed. Virtual environment is ready to use."
echo "Current PATH is: $PATH"

