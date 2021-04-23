import os
import pymongo
import shutil

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