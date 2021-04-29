Deployment
==========

Here is a complete example on how to setup and run a simple workflow via container-based approach - using Docker or Singularity.

Docker
------

.. _`Build the workflow-manager docker image`:

1. Build the workflow-manager docker image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build the docker image using ``dockerfile`` in ``/path/to/workflow-manager/docker/ubuntu``

#. Navigate to ``/path/to/workflow-manager``
#. Run

   .. code-block:: bash

      sudo docker build -f ./docker/ubuntu/Dockerfile --tag workflow-manager .

.. note::

   Below is the dockerfile we just used

   .. literalinclude:: ../../docker/ubuntu/Dockerfile
         :language: dockerfile

2. Run the docker image
^^^^^^^^^^^^^^^^^^^^^^^

* Run using docker command

   #. Create the following folders manually

      * dicom_node
      * test_project
      * mongodb
      * results

   #. Run

      .. code-block:: bash

         sudo docker run -p 8105:8105 -v /path/to/dicom_node:/dcmtk -v /path/to/test_project:/wm_project -v /path/to/mongodb:/mongodb/data/db -v /path/to/results:/results workflow-manager

      .. note::

         The results will be sent to the ``results`` folder.

   #. Stop the running containers

      #. Get container id

         .. code-block:: bash

            sudo docker ps

      #. Stop and delete the container

         .. code-block:: bash

            sudo docker rm -f <container_id>

* Run using docker-compose

   #. Navigate to ``/path/to/workflow-manager/docker/ubuntu/``
   #. Run

      .. code-block:: bash

         sudo docker-compose up

      .. note::

         If run the image this way, the results will be sent to a docker volume.
         The path to the volume would look similar to ``/var/lib/docker/volumes/ubuntu_results/_data``.
         You can use ``sudo docker volume ls`` to list all volumes.
         Then ``sudo docker volume inspect <volume_name>`` to find its actual location in the lost machine (see the value of the key ``Mountpoint``).

   #. Stop the running containers

      .. code-block:: bash

         sudo docker-compose stop

.. _`Trigger the data processing pipeline`:

3. Trigger the data processing pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Send dicom image(s) to trigger the workflow.
Here we use the DCMTK software to send dicom files.
To install DCMTK, run

   .. code-block:: bash

      sudo apt update
      sudo apt install -y dcmtk

* Send a single file

   .. code-block:: bash

      sudo storescu -v <ip_address> 8105 <file_path>

* Send a directory

   .. code-block:: bash

      sudo storescu -v <ip_address> 8105 --scan-directories <dir_path>

.. note::

   The result will be sent to the ``results`` folder/ docker volume depending on how you run the image.

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

#. Create the following folders manually

   * dicom_node
   * test_project
   * mongodb
   * results

.. code-block:: bash

   singularity run -B /path/to/dicom_node:/dcmtk:/dcmtk -B /path/to/test_project:/wm_project -B /path/to/mongodb:/mongodb/data/db -B /path/to/results:/results /path/to/workflow-manager.sif

3. Trigger the data processing pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`Trigger the data processing pipeline`