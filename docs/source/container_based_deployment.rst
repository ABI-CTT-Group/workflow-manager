Container-based deployment
==========================

Here is a complete example on how to setup and run a simple workflow via container-based approach.

* Run in :ref:`Docker`
* Run in :ref:`Singularity`

.. _Docker:

Docker
------

.. _`Getting the workflow-manager docker image`:

1. Getting the workflow-manager docker image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can get the docker image of workflow-manager by:

* :ref:`Pulling image from Docker Hub`
* :ref:`Building image from Dockerfile`

.. _`Pulling image from Docker Hub`:

Pulling image from Docker Hub
`````````````````````````````

.. code-block:: bash

   sudo docker pull clin864/workflow-manager

.. _`Building image from Dockerfile`:

Building image from Dockerfile
``````````````````````````````

Build the docker image from ``Dockerfile`` in ``/path/to/workflow-manager/docker/ubuntu``

#. Navigate to ``/path/to/workflow-manager``
#. Run

   .. code-block:: bash

      sudo docker build -f ./docker/ubuntu/Dockerfile --tag workflow-manager .

.. note::

   FYI, below is the dockerfile we just used.

   .. literalinclude:: ../../docker/ubuntu/Dockerfile
         :language: dockerfile

2. Run the docker image
^^^^^^^^^^^^^^^^^^^^^^^

* :ref:`Run the example workflow`
* :ref:`Run a custom workflow`

.. _`Run the example workflow`:

Run the example workflow
````````````````````````

#. Run the docker image:

   .. code-block:: bash

      sudo docker run -it -e MODE=examples workflow-manager


   .. note::

      The results will be saved in the ``results`` folder in the container we just launched using the docker run command.
      We can also map a folder inside a container to a local folder by adding a -v (or --volume ) argument to the run command.
      For example, ``sudo docker run -it -e RUN_EXAMPLES=TRUE -v /path/to/results:/results workflow-manager``

#. Stop the container. See :ref:`Stop a docker container`

.. _`Run a custom workflow`:

Run a custom workflow
`````````````````````

This docker image also allow you to run yor own workflow by passing the scripts, data and any resource the workflow will be using into the docker container.

#. Download and unzip the :download:`resource <./doc_downloads/resources.zip>` folder, and put all the input resources inside the folder.
   This resources folder contains:

   * ``./scripts``: folder which contains your custom scripts. Note that the scripts need to be converted/written in the format that the the workflow-manager supports. Please see this :ref:`Example Script` for reference.
   * ``./data``: folder where you put the input data
   * ``requirements.txt``: list all python dependencies of your scripts in this file
   * ``project_setup.py``: modify this script to set up your own workflow

      .. literalinclude:: ./doc_downloads/resources/project_setup.py
         :language: python

#. (optional) Create the following folders to save the project, database and results locally.
   In the next step, we will do folder mapping between local folders and the folders inside the container.
   Otherwise, you will lose all the data once the container is terminated.

   * project_folder/
   * database_folder/
   * result_folder/

#. Run the docker image

   .. code-block:: bash

      sudo docker run -v /path/to/resources:/resource -v /path/to/project_folder:/wm_project -v /path/to/database_folder:/mongodb/data/db -v /path/to/results:/results workflow-manager


   .. note::

      In the custom workflow, the final results will not automatically sent to the results folder.
      The results by default will just be save in the project workspace(s) depanding on how you set up your workflow.
      E.g ``/wm_project/workspaces/0003``
      You can either A. Map your local results folder to a final workspace
      or B. Send all the results from the project workspace(s) to the ``/results`` folder inside docker, then do a mapping between the local results folder and the results folder inside docker.

#. Stop the container. See :ref:`Stop a docker container`

.. _Stop a docker container:

3. Stop a docker container
^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Get container id

   .. code-block:: bash

      sudo docker ps

#. Stop and delete the container

   .. code-block:: bash

      sudo docker rm -f <container_id>

.. _Singularity:

Singularity
-----------

1. Build the Singularity image based on the pre-built docker image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. See :ref:`Build the workflow-manager docker image` to build the docker image.
#. Save the docker image as a .tar file

   .. code-block:: bash

      sudo docker save workflow-manager > workflow-manager.tar

#. Build the Singularity image from the pre-built docker image

   .. code-block:: bash

      singularity build workflow-manager.sif docker-archive://workflow-manager.tar

2. Run the Singularity image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``singularity run`` command is very similar to ``docker run``. Please have a look at the :ref:`Docker` section to get more ideas of how to run the example or a custom workflow.
For example, the docker ``-v`` argument needs to be replaced with the singularity ``-B`` when doing folder mapping.

* Run the example workflow

   .. code-block:: bash

      singularity run -shell --env MODE=examples workflow-manager

* Run a custom workflow

   .. code-block:: bash

      singularity run -B /path/to/resources:/resource -B /path/to/project_folder:/wm_project -B /path/to/database_folder:/mongodb/data/db -B /path/to/results:/results /path/to/workflow-manager.sif
