import sys
import pymongo

import workflow_manager

if __name__ == '__main__':
    if len(sys.argv) < 0:
        raise Exception('InputError.')
    project_name = sys.argv[1]
    project_root = sys.argv[2]
    script_dir = sys.argv[3]

    conn = pymongo.MongoClient('localhost', 27017)
    if not project_name in conn.list_database_names():
        print(conn.list_database_names())
        P = workflow_manager.create_project(project_name, root_dir=project_root)

        P.import_script(script_dir + '/pretend_import.py')
        P.import_script(script_dir + '/pretend_segment.py')
        P.import_script(script_dir + '/pretend_fit.py')
        P.import_script(script_dir + '/pretend_mechanics1.py')
        P.import_script(script_dir + '/pretend_mechanics2.py')
        P.import_script(script_dir + '/pretend_send.py')
