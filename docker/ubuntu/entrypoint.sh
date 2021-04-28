#!/bin/bash

set -m

# start mongodb and put it in the background
mongod --dbpath /mongodb/data/db --smallfiles &

# create a BPM project/pipeline
python3 $SCRIPTS/create_project.py $PROJECT_NAME $PROJECT_ROOT $EXAMPLES/scripts &

# set up a DICOM node and a post script listening to the node
storescp -v 8105 -tos 3 -dhl -ss dcm -tn --exec-on-eostudy "python3 $SCRIPTS/run_project.py #p $PROJECT_NAME"

# bring the primary (1st) process into the foreground
fg %1
