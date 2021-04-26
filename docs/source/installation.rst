Installation
============

Clone the GitHub repository:

.. code-block:: bash

   git clone https://github.com/physiome-workflows/workflow-manager.git

This is a private repository so you will need a GitHub account and have permissions to the repository.

Once cloned, you need to add the path to the workflow-manager(WM) module to your Python path environment variable. This can be added to your .bashrc file:

.. code-block::

   export PYTHONPATH=$PYTHONPATH:~/path_to_workflow-manager/workflow_manager

Requirements
------------

Please install the following packages

``pymongo`` - MongoDB is used for data storage.

Using Python virtual environment and the requirements.txt file to install packages is recommended.

#. Create a virtual environment

   .. code-block:: bash

      python3 -m venv venv/

#. Activate the virtual environment

   .. code-block:: bash

      source venv/bin/activate

#. Update pip

   .. code-block:: bash

      pip install --upgrade pip

#. Install the dependencies via requirements.txt

   .. code-block:: bash

      pip install -r requirements.txt
