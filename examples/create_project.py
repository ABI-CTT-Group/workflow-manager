import os
import pymongo
import shutil

import workflow_manager as wm

if __name__ == '__main__':
    project_name = 'test_project'
    project_root = './tmp/test_project'

    myclient = pymongo.MongoClient('localhost', 27017)
    if project_name in myclient.list_database_names():
        print('DROP %s database' % project_name)
        myclient.drop_database(project_name)
    if os.path.exists(project_root):
        print('DELETE %s directory' % project_root)
        shutil.rmtree(project_root)
    os.makedirs(project_root)

    P = wm.create_project(project_name, root_dir=project_root)

    P.import_script('scripts/pretend_import.py')
    P.import_script('scripts/pretend_segment.py')
    P.import_script('scripts/pretend_fit.py')
    P.import_script('scripts/pretend_mechanics1.py')
    P.import_script('scripts/pretend_mechanics2.py')
