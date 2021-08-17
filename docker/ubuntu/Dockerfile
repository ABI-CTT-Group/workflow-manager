ARG CODE_VERSION=18.04
FROM ubuntu:${CODE_VERSION}

USER root

# Environment variables
ENV MODULES_DIR /modules
ENV SCRIPTS /scripts
ENV PROJECT_NAME wm_project
ENV PROJECT_ROOT /$PROJECT_NAME
ENV DICOM_NODE /dcmtk/received
ENV EXAMPLES /examples
ENV RESULTS /results
ENV RESOURCES /resources

# Make dirs
RUN mkdir -p $MODULES_DIR
RUN mkdir -p $SCRIPTS
RUN mkdir -p $PROJECT_ROOT
RUN mkdir -p $DICOM_NODE
RUN mkdir -p /mongodb/data/db
RUN mkdir -p $RESULTS
RUN mkdir -p $RESOURCES

# Install system packages
RUN apt update && apt install -y \
    build-essential \
    cron \
    dcmtk \
    mongodb-server \
    python3.6 \
    python3.6-dev \
    python3-pip \
    python-psutil \
    python-pymongo \
    python-tables \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Copy files
ADD ./requirements.txt /requirements.txt
ADD ./docker/ubuntu/entrypoint.sh /entrypoint.sh
COPY ./docker/scripts $SCRIPTS
COPY ./examples $EXAMPLES

# Copy the custom packages to python site-package
COPY ./workflow_manager $MODULES_DIR/workflow_manager
RUN cp -R $MODULES_DIR/workflow_manager /usr/local/lib/python3.6/dist-packages

# Install Python dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r /requirements.txt

# Copy cron file to the cron.d directory
COPY ./docker/ubuntu/workflow-manager-cron /etc/cron.d/workflow-manager-cron
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/workflow-manager-cron
# Apply cron job
RUN crontab /etc/cron.d/workflow-manager-cron

WORKDIR $DICOM_NODE
CMD /bin/bash /entrypoint.sh

# How to build the image
# 1. navigate to /path/to/workflow-manager
# 2. sudo docker build -f ./docker/ubuntu/Dockerfile --tag workflow-manager .

# How to run the image
# 1. Create the following folders at any localtion:
#    - dicom_node
#    - test_project
#    - mongodb
#    - results
# 2. sudo docker run -p 8105:8105 -v /path/to/dicom_node:/dcmtk -v /path/to/test_project:/wm_project -v /path/to/mongodb:/mongodb/data/db -v /path/to/results:/results workflow-manager

# Run example pipeline
# - sudo docker run -it -e MODE=examples workflow-manager
# OR
# - sudo docker run -it -e MODE=examples -v /path/to/test_project:/wm_project -v /path/to/mongodb:/mongodb/data/db -v /path/to/results:/results workflow-manager
# Where:
#   - The environment variable RUN_EXAMPLES specify whether to run the example pipeline.
#   - Can also do folder mapping to save data locally (everything in docker will be deleted once the container is deleted). Some important folders in the docker images:
#       - /wm_project: the project root folder which contains three subfolders: 1. processes 2. scripts 3. workspaces
#       - /mongodb/data/db: the mongoDB database
#       - /results: the results folder can be used for storing the workflow results