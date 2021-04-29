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

# Make dirs
RUN mkdir -p $MODULES_DIR
RUN mkdir -p $SCRIPTS
RUN mkdir -p $PROJECT_ROOT
RUN mkdir -p $DICOM_NODE
RUN mkdir -p /mongodb/data/db
RUN mkdir -p $RESULTS

# Install system packages
RUN apt update
RUN apt install -y dcmtk
RUN apt install -y python3.6 build-essential python3.6-dev python3-pip
RUN apt install -y mongodb-server python-pymongo python-psutil python-tables

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