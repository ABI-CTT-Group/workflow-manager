# Physiome workflow manager

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/physiome-workflows/workflow-manager/blob/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/physiome-workflow-manager/badge/?version=latest)](https://physiome-workflow-manager.readthedocs.io/en/latest/)
[![Documentation Website](https://img.shields.io/website?down_color=red&down_message=down&up_color=brightgreen&up_message=up&url=https%3A%2F%2Fphysiome-workflow-manager.readthedocs.io%2Fen%2Flatest%2F)](https://physiome-workflow-manager.readthedocs.io/en/latest/)

[![Docker](https://img.shields.io/docker/pulls/clin864/workflow-manager.svg)](https://hub.docker.com/r/clin864/workflow-manager)
[![Image Size](https://img.shields.io/docker/image-size/clin864/workflow-manager/latest)](https://hub.docker.com/r/clin864/workflow-manager)

[![Repo Size](https://img.shields.io/github/repo-size/physiome-workflows/workflow-manager)](https://github.com/physiome-workflows/workflow-manager)
![Last Commit](https://img.shields.io/github/last-commit/physiome-workflows/workflow-manager)

![Python 3](https://img.shields.io/badge/Python->=3.6-blue)

An open-source software platform for creating and deploying Physiome-driven modelling workflows for research and clinical applications. It is a container based implemenation that provides infrastructure-agnostic software design that is intended to be hosted and executed entirely within research or hospital IT infrastructure.

## Dependencies

### Installing system dependencies

```commandline
apt update
apt install -y dcmtk python3.6 build-essential python3.6-dev python3-pip mongodb-server python-pymongo python-psutil python-tables
```

### Installing Python dependencies

```commandline
pip install -r requirements.txt
```

See requirements.txt for python dependencies.

## Accessing documentation

The documentation is hosted on Readthedocs https://physiome-workflow-manager.readthedocs.io

## Building documentation locally

### From the terminal
1. Clone the repository to your local machine.

2. Navigate to the docs/

3. Issue the command: `make html`

4. Open the index.html file in `docs/build/` folder

See the following [instructions](https://research-software-development-tutorials.readthedocs.io/en/latest/beginner/documenting_code/updating_documentation.html#updating-documentation) for more information regarding updating documentation.

## Contributing to documentation

### Updating the documentation
1. Fork this repository from an upstream repository to your github account (An Upstream repository is the Parent/Original repository from where you forked your repository)

2. Edit the restructuredText (.rst) or markdown (.md) files in the 
`docs/sources` folder (editing of these files can performed directly using the 
file editing tools provided by github. This will allow you to commit your 
changes to the repository.

3. Make a pull request from your fork to the master branch of the Upstream repository.

4. Your changes will be reviewed and pulled into the Upstream repository.

Over time, your fork may become out of sync with the master branch of the Upstream repository. Create a pull request on your fork to pull in the latest changes from the master branch of the Upstream repository to get your fork back up-to-date. This can be performed directly on the github website.


## Viewing the documentation

The full documentation can be found in the **docs/source** folder.
It's written in Sphinx format. 
You can also build the documentation locally, see [Sphinx's website](https://www.sphinx-doc.org/en/master/usage/quickstart.html) for the details of building the documentation.
