import imp
import os
import pymongo
import sys
import time

from workflow_manager.process import Process
from workflow_manager.script import Script
from workflow_manager.workspace import Workspace

"""
IDEAS:
- ancestors/parents/children/decendents
- register scripts with a version control system, i.e., can update via
  project and extract version id, etc...
- collections
- auto-update/stale data
- auto testing on script versions/sandpit
"""


def import_module(unique_name, path, module_name):
    """
    This is an old function that can be used to import a file as a module
    with a generic name.
    :param unique_name: unique name of the imported module
    :param path: path to the module
    :param module_name: module name
    """
    # sys.path.append(path)

    if unique_name in sys.modules:
        sys.modules.pop(unique_name)

    abspath = os.path.abspath(path)
    fp, pathname, description = imp.find_module(module_name, [abspath])
    # sys.path.remove(path)

    if os.path.exists(pathname):
        try:
            module = imp.load_module(unique_name, fp, pathname, description)
        except:
            print('Cannot open script {0}, check if it contains syntax errors ')
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()
    else:
        print('Cannot find script {0}')

    return module


def get_project_process(*args):
    if len(args) == 0:
        project_name = sys.argv[-2]
        process_id = sys.argv[-1]
    else:
        project_name = args[0]
        process_id = args[1]
    return Project(project_name).process(process_id)


class Project(object):
    def __init__(self, name, host='localhost', port=27017, user=None):
        client = pymongo.MongoClient(host, port)
        if name in client.list_database_names():
            self.db = client[name]
        else:
            raise Exception('Project %s does not exist' % name)

        self.name = name
        self.db_system = self.db['project'].system
        self.db_processes = self.db['project'].processes
        self.db_workspaces = self.db['project'].workspaces
        self.db_scripts = self.db['project'].scripts

        self.user = user
        if user is None:
            for key in ['USER', 'USERNAME']:
                if key in os.environ.keys():
                    self.user = os.environ.get(key)
                    break

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print_str = ""
        results = self.db_processes.find(limit=50).sort(
            'id', pymongo.DESCENDING)
        for cursor in results:
            process = self.process(cursor['id'])
            print_str += process.__str__() + '\n'
        return print_str

    @property
    def root_dir(self):
        result = self.db_system.find_one({'key': 'root_dir'})
        if result != None:
            return result['path']

    @property
    def scripts_dir(self):
        scripts_dir = self.db_system.find_one({'key': 'scripts_dir'})
        return os.path.join(self.root_dir, scripts_dir['path'])

    @property
    def processes_dir(self):
        return os.path.join(self.root_dir, 'processes')

    @property
    def workspaces_dir(self):
        workspaces_dir = self.db_system.find_one({'key': 'workspaces_dir'})
        return os.path.join(self.root_dir, workspaces_dir['path'])

    def processes(self, label=None, status=None, limit=0):
        processes = []
        search_dict = {}
        if label is not None:
            search_dict['label'] = label
        if status is not None:
            search_dict['status'] = status

        if len(search_dict.keys()):
            for cursor in self.db_processes.find(search_dict, limit=limit).sort(
                    'id', pymongo.DESCENDING):
                processes.append(self.process(cursor['id']))
        else:
            for cursor in self.db_processes.find(limit=limit).sort(
                    'id', pymongo.DESCENDING):
                processes.append(self.process(cursor['id']))
        return processes

    def process_path(self, path, base_path=None):
        if not os.path.isabs(path):
            if base_path is None:
                base_path = self.root_dir
            path = os.path.join(base_path, path)
            path = os.path.normpath(path)
        return path

    def _new_script_id(self):
        self.db_system.update({'key': 'script_index'}, {'$inc': {'index': 1}})
        return self.db_system.find_one({'key': 'script_index'})['index']

    def _new_process_id(self):
        self.db_system.update({'key': 'process_index'}, {'$inc': {'index': 1}})
        return self.db_system.find_one({'key': 'process_index'})['index']

    def _new_workspace_id(self):
        self.db_system.update({'key': 'workspace_index'}, {'$inc': {'index': 1}})
        return self.db_system.find_one({'key': 'workspace_index'})['index']

    def trim_process_index(self):
        p = self.db_processes.find_one(sort=[("id", -1)])
        index = self.db_system.find_one({'key': 'process_index'})['index']
        if p['id'] < index:
            self.db_system.update({'key': 'process_index'}, {'$set': {'index': p['id']}})

    def trim_script_index(self):
        s = self.db_scripts.find_one(sort=[("id", -1)])
        index = self.db_system.find_one({'key': 'script_index'})['index']
        if s['id'] < index:
            self.db_system.update({'key': 'script_index'}, {'$set': {'index': s['id']}})

    def trim_workspace_index(self):
        w = self.db_workspaces.find_one(sort=[("id", -1)])
        index = self.db_system.find_one({'key': 'workspace_index'})['index']
        if w['id'] < index:
            self.db_system.update({'key': 'workspace_index'}, {'$set': {'index': w['id']}})

    def clear_db(self):
        self.db_workspaces.drop()
        self.db_processes.drop()

    def clear_workspaces(self):
        self.db_workspaces.drop()

    def clear_system(self):
        self.db_system.drop()

    def new_script(self, label):
        return Script(self, label, create=True)

    def delete_script(self, label):
        s = self.script(label)
        self.db_scripts.remove({'id': s.id})
        self.trim_script_index()

    def get_script(self, script_id):
        print('Deprecated, use script(script_id) instead.')
        return self.script(script_id)

    def script(self, script_id, can_create=False):
        script = Script(self, script_id)
        if script.id is not None:
            return script
        else:
            return self.new_script(script_id)

    def import_script(self, path, script_id=None, rerun_processes=False):
        if '/' not in path:
            path = './' + path
        spath = path.split('/')
        module_name = os.path.splitext(spath.pop())[0]
        spath = '/'.join(spath)
        script_module = import_module('bpm_import_script_tmp', spath, module_name)
        if script_id is not None:
            script = self.script(script_id, True)
        else:
            script = self.script(script_module.script_id, True)
        script.set_data('import_path', os.path.abspath(path))
        script.set_source_path(spath)
        script.update_from_source()

        # Check for and instantiate new dependent processes
        for dep in script.data['dependent_on']:
            for process in self.processes(dep):
                decendents = process.get_decendents(script.label)
                print(dep, process.id, decendents)
                if len(decendents) == 0:
                    script.run({}, parent_id=process.id)
                elif rerun_processes:
                    for decendent in decendents:
                        decendent.queue()

        return script

    def run_script(self, label, params):
        script = self.script(label)
        script.run(params=params)

    def list_scripts(self):
        for cursor in self.db_scripts.find():
            # print cursor
            print(cursor['id'], cursor['label'], cursor['source_path'])

    def new_workspace(self, label=None):
        return Workspace(self, label=label)

    def get_workspace(self, wksp_num):
        print('Deprecated. Use workspace(wksp_num) instead.')
        return self.workspace(wksp_num)

    def delete_workspace(self, id):
        self.db_workspaces.remove({'id': id})
        self.trim_workspace_index()

    def workspace(self, wksp_num):
        return Workspace(self, wksp_num)

    def list_workspaces(self):
        for cursor in self.db_workspaces.find():
            print(cursor)

    def get_process(self, pid):
        print('Deprecated: use process(pid) instead')
        return self.process(pid)

    def process(self, pid):
        return Process(self, pid)

    def delete_process(self, pid, delete_workspaces=True):
        p = self.process(pid)
        if delete_workspaces:
            workspaces = p.get_workspaces()
            for w in workspaces:
                w.delete_folder()
                self.db_workspaces.remove({'id': w.id})
                self.trim_workspace_index()
        self.db_processes.remove({'id': p.id})
        self.trim_process_index()

    def queue(self, process_id, propagate=False):
        if not isinstance(process_id, list):
            process_id = [process_id]
        for pid in process_id:
            proc = self.process(pid)
            if proc != None:
                proc.queue(propagate=propagate)
            else:
                print("Process %d not found" % (pid))

    def kill(self, process_id):
        proc = self.process(process_id)
        if proc != None:
            proc.kill()
        else:
            print("Process %d not found" % (process_id))

    def kill_all(self):
        for proc in self.processes(status='pending'):
            proc.kill()
        for proc in self.active_processes:
            proc.kill()

    def list(self, arg=None, limit=40, script=None, sort=pymongo.DESCENDING):
        self.list_processes(arg=arg, limit=limit, script=script, sort=sort)

    def list_processes(self, arg=None, limit=40, script=None, sort=pymongo.DESCENDING):
        if isinstance(arg, int):
            limit = arg
        elif isinstance(arg, str):
            script = arg

        if script != None:
            results = self.db_processes.find({'script': script}, limit=limit).sort(
                'id', pymongo.DESCENDING)
        else:
            results = self.db_processes.find(limit=limit).sort(
                'id', pymongo.DESCENDING)
        for cursor in results:
            process = self.process(cursor['id'])
            print(process)

    @property
    def processes_pending(self):
        dbproc = self.db_processes.find_one({'status': 'pending'})
        if dbproc is None:
            return False
        return True

    @property
    def active_process(self):
        dbproc = self.db_processes.find_one({'status': 'processing'})
        if dbproc is not None:
            return Process(self, dbproc['id'])
        return None

    @property
    def active_processes(self):
        dbprocs = self.db_processes.find({'status': 'processing'})
        processes = []
        for dbproc in dbprocs:
            processes.append(Process(self, dbproc['id']))
        return processes

    @property
    def total_used_cores(self):
        dbprocs = self.db_processes.find({'status': 'processing'})
        used_cores = 0
        if dbprocs.count() > 0:
            for dbproc in dbprocs:
                proc = Process(self, dbproc['id'])
                used_cores += proc.cores
        return used_cores

    def start_next_process(self):
        dbprocs = self.db_processes.find({'status': 'pending'}, limit=1).sort(
            'id', pymongo.ASCENDING)

        if dbprocs.count() == 0:
            dbproc = None
        else:
            dbproc = dbprocs[0]

        process = None
        if dbproc is not None:
            process = Process(self, dbproc['id'])
        if process is not None:
            process.start()

    def get_next_process(self, unused_cores=None):
        dbprocs = self.db_processes.find({'status': 'pending'}).sort(
            'id', pymongo.ASCENDING)

        # No pending processes
        if dbprocs.count() == 0:
            return None

        # Return first process independent of the number of cores required
        if unused_cores == None:
            return Process(self, dbprocs[0]['id'])

        # Return first process that fits into the unused cores
        for dbproc in dbprocs:
            proc = Process(self, dbproc['id'])
            if proc.cores <= unused_cores:
                return proc

    def process_completed(self, proc_id):
        process = Process(self, proc_id)
        process.completed()

    def check_active_process(self):
        process = self.active_process
        if process is not None:
            process.check_status()

    def check_active_processes(self):
        processes = self.active_processes
        for process in processes:
            if process is not None:
                process.check_status()


def start_process_monitor(project_name, minutes_alive=10, sleep_time=3, total_cores=1):
    """
    This script monitor the a job queue in the web2py database. If it finds
    pending jobs it runs the job and monitors it for success or failure and
    updates the database.

    To create a cron for the job monitor add the following to your contab (crontab -e):
    */10 * * * * python /path_to_bpm/project.py project_name >> /home/malcolm/log.cron

    """

    project = Project(project_name)
    minutes_alive = minutes_alive  # minutes before the loop below completes
    sleep_time = sleep_time  # seconds between checks
    # Records the start time such that this function can operate for a
    # specific time and then quit.
    # The system cron will reactivate it 5 seconds later.

    seconds_alive = 60 * minutes_alive - 5  # i.e., die 5 seconds before next cron job starts
    start_time = time.time()
    loop_count = 0
    while time.time() - start_time < seconds_alive:
        loop_count += 1
        ### Check for jobs to kill
        # ~ for job in workspace.jobs_to_kill:
        # ~ job.kill()

        # Check jobs that are processing for failures or timeouts
        project.check_active_processes()

        # Start new jobs. Loops until as much of the available cores
        # are used.
        unused_cores = total_cores - project.total_used_cores
#        print "Loop %d (Active cores: %d/%d)" % (loop_count, project.total_used_cores, total_cores)

        while unused_cores > 0:
            process = project.get_next_process(unused_cores)
            if process != None:
                print("Starting process " + str(process.id))
                process.start()
                unused_cores = total_cores - project.total_used_cores
            else:
                break

        # If there are no processes running, checks if there is a
        # process that require more cores than are available
        # and runs it
        if project.total_used_cores == 0:
            process = project.get_next_process()
            if process != None:
                print("Running a process that requires more cores than allocated")
                process.start()

        time.sleep(sleep_time)  # retry in


if __name__ == "__main__":
    project_name = sys.argv[1] if len(sys.argv) > 1 else None
    minutes_alive = float(sys.argv[2]) if len(sys.argv) > 2 else 10
    sleep_time = float(sys.argv[3]) if len(sys.argv) > 3 else 3
    total_cores = float(sys.argv[4]) if len(sys.argv) > 4 else 1
    if project_name is None:
        raise Exception('Project name required')
    else:
        start_process_monitor(project_name, minutes_alive, sleep_time, total_cores)
