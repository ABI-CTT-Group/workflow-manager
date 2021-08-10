#!/bin/bash

#set -m
#
# start mongodb and put it in the background
#mongod --dbpath /mongodb/data/db --smallfiles &
#
## create a new project/pipeline
#python3 $SCRIPTS/create_project.py $PROJECT_NAME $PROJECT_ROOT $EXAMPLES/scripts &
#
## set up a DICOM node and a post script listening to the node
#storescp -v 8105 -tos 3 -dhl -ss dcm -tn --exec-on-eostudy "python3 $SCRIPTS/run_project.py #p $PROJECT_NAME"
#
## bring the primary (1st) process into the foreground
#fg %1

#start mongodb and put it in the background
mongod --dbpath /mongodb/data/db --smallfiles --fork  --logpath /var/log/mongodb/mongod.log &

if [[ "${MODE,,}" == "examples" ]]; then
  echo 'Running the example pipeline'
  python3 ${SCRIPTS}/create_project.py ${PROJECT_NAME} ${PROJECT_ROOT} $EXAMPLES/scripts
  python3 ${SCRIPTS}/run_project.py ${EXAMPLES}/data/pretend_data.txt ${PROJECT_NAME}
fi

if [[ "${MODE,,}" == "dicom" ]]; then
    echo "starting dicom node"
    python3 ${RESOURCES}/create_project.py ${PROJECT_NAME} ${PROJECT_ROOT} ${RESOURCES}/scripts
    storescp -v 8105 -tos 3 -dhl -ss dcm -tn --exec-on-eostudy "python3 ${RESOURCES}/run_project.py #p ${PROJECT_NAME}"

#    # create a new project/pipeline
#    python3 ${SCRIPTS}/create_project.py ${PROJECT_NAME} ${PROJECT_ROOT} ${EXAMPLES}/scripts
#    # set up a DICOM node and a post script listening to the node
#    storescp -v 8105 -tos 3 -dhl -ss dcm -tn --exec-on-eostudy "python3 ${SCRIPTS}/run_project.py #p ${PROJECT_NAME}"
fi

if [[ "${MODE,,}" == "custom" ]]; then
  python3 ${RESOURCES}/project_setup.py ${PROJECT_NAME} ${PROJECT_ROOT} ${RESOURCES}
fi


