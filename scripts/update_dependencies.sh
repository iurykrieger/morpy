#!/bin/bash

# Updates 'morpy' dependencies
conda install -y --file conda-requirements.txt
source activate morpy
pip install -r requirements.txt