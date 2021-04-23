import os
import pymongo
import time

def create_project(name, root_dir='.', host='localhost', port=27017):
    """
    Creates a new project.

    :param name:
        the name of the project, which must be unique in the
        MongoDB used by the project.
    :param root_dir:
        the root directory for the project. If the folder does not
        exist it will be created. Three additional subdirectories
        will be created: scripts, workspaces and logs.
    :param host: the `host` for the MongoDB database.
    :param port: the `port` for the MongoDB database.

    :returns: Project
    """

    from workflow_manager.project import Project

    scripts_dir = 'scripts'
    workspaces_dir = 'workspaces'

    # Check db does not exist
    client = pymongo.MongoClient(host, port)
    if name not in client.list_database_names():

        # Check root directory does not exist
        root_abs_dir = os.path.abspath(root_dir)
        if not os.path.exists(root_abs_dir):
            os.makedirs(root_abs_dir)

        # Check and create scripts directory
        if os.path.isabs(scripts_dir):
            scripts_full_path = scripts_dir
        else:
            scripts_full_path = os.path.join(root_abs_dir, scripts_dir)

        if not os.path.exists(scripts_full_path):
            os.makedirs(scripts_full_path)

        procs_dir = os.path.join(root_abs_dir, 'processes')
        if not os.path.exists(procs_dir):
            os.makedirs(procs_dir)

        # Check and create workspaces directory
        if os.path.isabs(workspaces_dir):
            workspaces_full_path = workspaces_dir
        else:
            workspaces_full_path = os.path.join(root_abs_dir, workspaces_dir)

        if not os.path.exists(workspaces_full_path):
            os.makedirs(workspaces_full_path)

        # Create database
        db = client[name]
        collection = db['project'].system
        collection.insert_one({'key': 'workspace_index', 'index': 0})
        collection.insert_one({'key': 'script_index', 'index': 0})
        collection.insert_one({'key': 'process_index', 'index': 0})
        collection.insert_one({'key': 'root_dir', 'path': root_abs_dir, 'is_absolute_path': True})
        collection.insert_one({'key': 'scripts_dir', 'path': scripts_dir})
        collection.insert_one({'key': 'workspaces_dir', 'path': workspaces_dir})

    else:
        raise Exception('Database %s already exist' % name)

    project = Project(name)
    # Check and delay until project is created.
    while project.root_dir is None:
        time.sleep(0.01)
    return project


def drop_database(name, host='localhost', port=27017):

    from workflow_manager.project import Project

    client = pymongo.MongoClient(host, port)
    if name in client.list_database_names():
        project = Project(name)
        root_dir = project.root_dir
        client.drop_database(name)
        print('%s database has been deleted, the root directory (%s) was not touched.' % (name, root_dir))

    else:
        raise UserWarning('Database %s not found' % name)


def pretty_time(dt):
    """
    Returns a human readable string for a time duration in seconds.
    :param dt: duration in seconds
    """
    if dt > 3600:
        hours = dt / 3600.
        if hours > 9:
            return '%dh' % (int(hours))
        minutes = 60 * (hours - int(hours))
        return '%dh%2dm' % (int(hours), int(minutes))
    elif dt > 60:
        minutes = dt / 60.
        if minutes > 9.5:
            return '%dm' % (int(minutes))
        seconds = 60 * (minutes - int(minutes))
        return '%dm%2ds' % (int(minutes), int(seconds))
    elif dt > 10:
        return '%ds' % (int(dt))
    elif dt > 0.05:
        return '%4.1fs' % dt
    else:
        return '-'
