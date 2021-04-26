Examples
========

To run the examples,
you first need to install the package
and add the path to the package to your PYTHONPATH environment variable (see the installation page).

Example Scripts
---------------

There are some usage examples of the workflow-manager package:

* ``create_project.py``

   Create a WM project in ``./tmp/test_project/`` and import some mock scripts into the project.

* ``run_project.py``

   Put the scripts of the example project into a queue and run the project.
   This will also start a process monitor for the project.
   If it finds pending jobs it runs the job and monitors it for success or failure and
   updates the database.

* ``create_and_run.py``

   Create and run a example project.

* ``monitor_project.py``

   Monitor the example project status by listing the imported scripts and their status - success or failure.

* ``delete_project.py``

   Delete the example project

Others
------

* To look at the processes of a given project, type

   .. code-block:: python

      import workflow_manager
      P = workflow_manager.Project('project_name')
      P.list_processes()

* To look at a given processes log, type

   .. code-block:: python

      import workflow_manager
      P = workflow_manager.Project('project_name')
      P.process(process_id).log()
