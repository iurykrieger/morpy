#!/bin/bash

# Install mongodb
echo "# Installing mongodb"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Creates mongo database folder
sudo mkdir -p /data/db

# Install python pip if it doesn't exists
echo "# Installing python pip..."
sudo apt-get install python-pip

# Creates 'morpy' venv and install all it's requirements
echo "# Creating python virtual envroinment..."
conda env remove -n morpy -y
conda create -n morpy -y --file conda-requirements.txt
source activate morpy
pip install -r requirements.txt