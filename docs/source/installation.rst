.. _Installation:

Installation
============

This page shows how to install the workflow-manager as a Python package in your python environment.
Once installed, you can use import it by adding ``import workflow_manager`` in your code.


Prerequisites
-------------
Please install the following system packages

* ``mongodb-server`` - MongoDB is used for data storage.

.. code-block:: bash

   apt update
   apt install -y dcmtk python3.6 build-essential python3.6-dev python3-pip mongodb-server python-pymongo python-psutil python-tables

Installation steps
------------------

#. Clone the GitHub repository:

   .. code-block:: bash

      git clone https://github.com/physiome-workflows/workflow-manager.git

   .. note::

      This is a private repository so you will need a GitHub account and have permissions to the repository.

#. Add workflow-manager(WM) to Python environment

   Once cloned, you need to add the path to the workflow-manager(WM) module to your Python path environment variable.
   This can be added to your ~/.bashrc file.

   .. code-block::

      export PYTHONPATH=$PYTHONPATH:~/path_to_workflow-manager/workflow_manager

   .. note::

      Once saved, you can run ``echo $PYTHONPATH`` to see if the path has been added to PYTHONPATH.
      If not, you might need to reload the .bashrc file by ``source ~/.bashrc`` or open a new terminal session.

#. Install Python dependencies

   Using Python virtual environment is recommended.
   Below shows the steps to install the dependencies from the dependency file requirements.txt into a python virtual environment.

   #. Create a virtual environment

      .. code-block:: bash

         python3 -m venv venv/

   #. Activate the virtual environment

      .. code-block:: bash

         source venv/bin/activate

      .. note::

         To deactivate a virtual environment, run

         .. code-block:: bash

            deactivate

   #. Update pip

      .. code-block:: bash

         pip install --upgrade pip

   #. Install the dependencies via requirements.txt

      .. code-block:: bash

         pip install -r requirements.txt
