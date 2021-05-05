Projects
========

.. module:: workflow_manager

Projects, the top level object in workflow_manager(WM), holds all the scripts, processes,
and workspace data.


Creating Projects
-----------------

A new project can be created by

.. code-block:: python

   import workflow_manager
   P = workflow_manager.create_project('myProject', './path/to/project_datastore')

This call will assume the MongoDB is installed on the local machine and
use the default MongoDB port. If a remote database or different port is
used then this can be defined using the keyword arguments.

.. automodule:: workflow_manager
   :members: create_project


Retrieving a Project
--------------------

A project can be retrieved by:

.. code-block:: python

   import workflow_manager
   P = workflow_manager.Project('myProject')

Using a Project
---------------

