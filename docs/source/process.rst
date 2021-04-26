Processes
=========

.. module:: workflow_manager

A process is the execution of a script. This typically creates workspaces
and generates new data.

The list of processes associated with a project can be retrieved by calling,

.. code-block:: python

   project.list_processes()

A process can be retrieved from the project by calling,

.. code-block:: python

   process = project.get_process(process_id)

The parent process which spawned a process is given by the attribute,

.. code-block:: python

   process.parent_process

The data and arguments associated with a process is given by,

.. code-block:: python

   process.data
   process.arguments

A process can be controlled using the following functions:

.. code-block:: python

   process.start()
   process.queue()
   process.completed(status=True, message="")
   process.kill()

The start function will execute the script. Typically, you will not need
to run this command to start a process since there will be a job monitor
running that monitors the queue for pending processes and runs them sequentially.

The queue function will add the process to the job monitor queue if it
is not in the queue already. This function will allow you to rerun a process
in the case of a failure and the source of the failure has been fixed.

The completed function is required in script to inform the process of the
outcome of executing the script. This function takes two arguments, status
which is True for success or False for failure, and message which is an
optional argument that may describe, for example, the reason for failure.

The kill function will kill the process if it is executing otherwise
remove it as a pending job in the queue.

Workspaces associated with a process can be created or retrieved by
calling,

.. code-block:: python

   workspace = process.get_workspace(label)

If the workspace with the given label does not exists for the process it
will be created. It is important to use this function in scripts as it
will record the relationship between processes and workspaces.
