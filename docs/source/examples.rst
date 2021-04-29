Examples
========

This section shows some usage examples on how to create a project, add some scripts with
dependencies, and run a parent script that creates a pipeline of processes.

Make sure you have everything setup before moving down, see :ref:`Installation`.

Example Scripts
---------------

There are some pre-built example scripts in the ``examples`` folder under the root of the workflow-manager repository - ``/path/to/workflow-manager/examples``

* ``create_and_run_project.py``

   Create and run a example project.

   .. literalinclude:: ../../examples/create_and_run_project.py
      :language: python

* ``create_project.py``

   Create a WM project in ``/path/to/workflow-manager/examples/tmp/test_project/`` and import some mock scripts into the project.

   .. literalinclude:: ../../examples/create_project.py
      :language: python

* ``run_project.py``

   Put the scripts of the example project into a queue and run the project.
   This will also start a process monitor for the project.
   If it finds pending jobs it runs the job and monitors it for success or failure and
   updates the database.

   .. literalinclude:: ../../examples/run_project.py
      :language: python

* ``monitor_project.py``

   Monitor the example project status by listing the imported scripts and their status - success or failure.

   .. literalinclude:: ../../examples/monitor_project.py
      :language: python

* ``delete_project.py``

   Delete the example project

   .. literalinclude:: ../../examples/delete_project.py
      :language: python

Other usage examples
--------------------

* Create a WM project

   .. code-block:: python

      import workflow_manager
      P = workflow_manager.create_project('my_project', './path/to/project_datastore')

* Add scripts to the project

   .. code-block:: python

      P = workflow_manager.create_project(project_name, root_dir=root)
      P.import_script('/path/to/scripts_1.py')
      P.import_script('/path/to/scripts_2.py.py')
      P.import_script('/path/to/scripts_3.py.py')

   You can can set script dependency by

   .. code-block:: python

      script = P.script('child_script')
      script.add_dependency('parent_script')

   or by specifying ``depends_on = ['parent_script']`` at the beginning of the child script

   Both will run the child script after the completion of the parent script.

* Create processes from imported scripts and put them into a project queue. The code below will generate processes for the ``pretend_import`` script and its child scripts.

   .. code-block::

      script = P.script('pretend_import')
      script_input_arguments = {'path': 'data/pretend_data.txt'}
      script.run(script_input_arguments)

* Start process monitor

   Start a process monitor to actually run and monitor the processes in the project queue.

   .. code-block:: python

      workflow_manager.project.start_process_monitor(project_name, minutes_alive=3, sleep_time=3, total_cores=8)

* To look at the processes of a given project, type

   .. code-block:: python

      P = workflow_manager.Project('project_name')
      P.list_processes()

* To look at a given processes log, type

   .. code-block:: python

      P = workflow_manager.Project('project_name')
      P.process(process_id).log()
