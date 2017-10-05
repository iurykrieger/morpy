#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Configure env
printf "${GREEN}\n# Configuring envorinment...\n${NC}"
cp .env.example .env

# Install mongodb
printf "${GREEN}\n# Installing mongodb...\n${NC}"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Creates mongo database folder
printf "${GREEN}\n# Configuring mongodb data folder...\n${NC}"
sudo mkdir -p /data/db
sudo chown -R $USER /data/db

# Install python pip if it doesn't exists
printf "${GREEN}\n# Installing python pip...\n${NC}"
sudo apt-get install python-pip

# Creates 'morpy' venv and install all it's requirements
printf "${GREEN}\n# Creating and configuring conda virtual envroinment...\n${NC}"
conda env remove -n morpy -y
conda create -n morpy -y --file conda-requirements.txt
source activate morpy
pip install -r requirements.txt

printf "${GREEN}\n# All done! Now you can configure morpy and start it by executing start.sh!${NC}"