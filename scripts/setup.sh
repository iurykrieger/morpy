#!/bin/bash

# Install python pip if it doesn't exists
echo "# Installing python pip..."
sudo apt-get install python-pip

# Install all global requirements before conda
echo "# Installing all global requirements..."
pip install -r requirements.txt

# Creates 'morpy' venv and install all it's requirements
echo "# Creating python virtual envroinment..."
conda create -n morpy --file conda-requirements.txt