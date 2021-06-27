Workspaces
==========

Workspaces stores files and data.

To create a new workspace:

.. code-block:: python

   workspace = project.new_workspace(label='optional_label')

To load a workspace:

.. code-block:: python

   workspace = project.load_workspace(workspace_id)

The workspace has a couple of useful attributes:

.. code-block:: python

   workspace.id # prints the unique id of the workspace
   workspace.path # path to the workspace folder

The idea is that you can use the workspace.path to create or copy files
to. There is a convenient function to open files in the workspace:

.. code-block:: python

   fp = workspace.open_file(filename, mode='w')
   fp.write("some text")
   fp.close()

The open_file function will return a Python pointer to a file.

This file can later be opened by:

.. code-block:: python

   fp = workspace.open_file(filename)
    
where the read/write mode defaults to read (mode='r').

In addition to file based data, data in the form of a dictionary can be
added to the workspace:

.. code-block:: python

   workspace.add_data({'technique': 'pid controller', 'params':[0.4, 0.2, 1.4]})

A file can be copied into a workspace by calling the following command,

.. code-block:: python

   status, message = workspace.copy_file(filepath)

The filepath is the path to the file to be copied into the workspace.
This can the absolute path or relative path to the root directory of
the project. The variables, status and message, return the success or
failure state of the copy and an associated message.

A zip file can be extracted into a workspace by,

.. code-block:: python

   status, message = workspace.extract_zip(filepath)

The filepath is the path to the zip file to be copied into the workspace.
This can the absolute path or relative path to the root directory of the
project. The variables, status and message, return the success or failure
state of the copy and an associated message.

.. note::

   At the moment this is an ad hoc implementation of a workspace.
   The hope is that this will evolve into a simple and generic method for
   storing blocks of data, be it text or binary files or key/value pairs of
   data. See the Future Ideas section for more discussion.
