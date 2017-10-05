#!/bin/bash

# Seeds data from MovieLens dataset
MAIN_PATH=$(pwd)

echo "Downloading Movie Lens dataset"
cd storage &&
curl -sS http://files.grouplens.org/datasets/movielens/ml-1m.zip > ml-1m.zip &&
unzip ml-1m.zip &&
rm ml-1m.zip &&
sed -i -- 's/::/:/g' ml-1m/*

cd $MAIN_PATH

echo "Populating database with Movie Lens dataset"
source activate morpy
python -m database.seed.seed

echo "Database seeded!"