#!/bin/sh

# Install python pip if it doesn't exists
sudo apt-get install python-pip

# Install all global requirements before conda
pip install -r requirements.txt

# Creates 'morpy' venv and install all it's requirements
conda create -n morpy --file conda-requirements.txt