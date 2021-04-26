Example
=======

.. module:: workflow_manager

Here is a full example on how to create a project, add some scripts with
dependencies, and run a parent script that creates a pipeline of processes.
For more details, see `root/examples/ <https://github.com/LIN810116/workflow-manager/tree/main/examples>`_.

.. code-block:: python

   import os
   import pymongo
   import shutil

   import workflow_manager as wm

   if __name__ == '__main__':
       project_name = 'test_project'
       root = './tmp/test_project'

       myclient = pymongo.MongoClient('localhost', 27017)
       if project_name in myclient.list_database_names():
           print('DROP %s database' % project_name)
           myclient.drop_database(project_name)
       if os.path.exists(root):
           print('DELETE %s directory' % root)
           shutil.rmtree(root)
       os.makedirs(root)

       P = wm.create_project(project_name, root_dir=root)
       P.import_script('scripts/pretend_import.py')
       P.import_script('scripts/pretend_segment.py')
       P.import_script('scripts/pretend_fit.py')
       P.import_script('scripts/pretend_mechanics1.py')
       P.import_script('scripts/pretend_mechanics2.py')

       script = P.script('import')
       script_input_arguments = {'path': 'data/pretend_data.txt'}
       script.run(script_input_arguments)

       wm.project.start_process_monitor(project_name, minutes_alive=3, sleep_time=3, total_cores=8)
