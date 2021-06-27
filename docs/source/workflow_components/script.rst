Scripts
=======

A script is a description of how to process data. Scripts can depend on
other scripts which create pipelines of processes.

Adding a Script to a Project
----------------------------

To add a script to a project, you need to create a new script with a 
unique label within the project, set the program command to execute the
script and path to the script. The path can be an absolute or relative
path. A relative path is with respect to the script directory. In the
case of a relative path, the script needs to be copied to the projects
scripts directory.

An example of adding a script to a project,

.. code-block:: python

   script = project.new_script('import scan')
   script.set_program('python')
   script.set_script('import_scan.py')

.. _Script Dependencies:

Script Dependencies
-------------------

A dependency on another script can be added using the add_dependency
function with the label of the parent script. For example, this segment
script depends on the  pretend import script, 

.. code-block:: python

   script = project.new_script('segment')
   script.set_program('python')
   script.set_script('segment.py')
   script.add_dependency('pretend_import')

In this case, on completion of any process that is spawned from the
import scan script, the segment script will spawn a process with a
relationship to the parent process. This allow pipelining of processes
and the automatic recording and tracing of data processing.

 
Updating Scripts from Sources
-----------------------------

Instead of manually copying a script to the projects script directory,
the source of the script can be defined using the add_source function
and the update_from_source function can be called to copy the script
into the projects scripts directory. For example,

.. code-block:: python

   script.add_source('/home/user/my_scripts/import_scan.py')
   script.update_from_source()

A script can have multiple source files, for example, supporting
modules. Currently, this feature only supports copy updates but is
intended to include http and versioned repository type sources. In all
cases, a version can be associated with the script and processes spawned
from the script such that the processes that create data can be
traceable. This means the exact processes that created some data can be
traced back to its origin.


Running a Script
----------------

This script can be run manually or automatically by a cron job or the
WM project due to a dependency. Here is an example of how to manually
run this script:

.. code-block:: python

   project = workflow_manager.Project(project_name)
   project.run_script('import_zipped_scan', {'filepath':zippath})

First, load the project then run the run_script function which takes the
script label (‘import_zipped_scan’) and script arguments as inputs. This
will create a process that executes the script in the project
environment.

.. _Example Script:

Example Script
--------------

Here is an example of the Import scan script:

.. code-block::

   import sys
   import workflow_manager

   def run(project_name, process_id):

      # Open project
      project = workflow_manager.Project(project_name)
      
      # Get process and arguments
      process = project.get_process(process_id)
      filepath = process.arguments.get('filepath')
      
      # Create or load workspace
      workspace = process.get_workspace('scan')
      
      # Extract zip file into workspace
      status, message = workspace.extract_zipfile(filepath)
      process.completed(status, message) ### REQUIRED ###

   if __name__ == "__main__":
          project_name = sys.argv[-2]
          process_id = sys.argv[-1]
          run(project_name, process_id)

When this script is run, it requires the project name and the process id
that is running this script. Given these arguments:

   #. the project is opened
   #. the process running the script is loaded
   #. the path to the zip file, the filepath argument is retrieved from the process
   #. a workspace called scan (required) is created or retrieved if it exists
   #. the zip file is extracted into the workspace
   #. and the status of the process is returned to the process - this will spawn any dependent scripts.

Notice the example script has a run function that is called from a
``if __name__ == “__main__”:`` expression. This allows a script to be
called from the command line and, in the future, by importing the script
as a module. So it is good practice to write your scripts to include a
run function, i.e., in the form above.
