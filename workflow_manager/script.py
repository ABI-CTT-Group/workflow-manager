import imp
import os
import shutil

import sys

import time


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

    try:
        module = imp.load_module(unique_name, fp, pathname, description)
    except:
        pass
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()

    return module


class Script(object):
    def __init__(self, project, label, create=False):

        self.project = project
        self.label = label
        self.id = None
        if create:
            self._new()
        else:
            self._load()

    @property
    def data(self):
        return self.project.db_scripts.find_one({'id': self.id})

    @property
    def path(self):
        return os.path.join(self.directory, self.data['filename'])


    @property
    def directory(self):
        return os.path.join(self.project.scripts_dir, '%04d' % self.id)

    def _new(self):
        """
        Creates a new script

        Return script_id
        """
        existing_document = self.project.db_scripts.find_one(
            {'label': self.label})

        if existing_document is None:
            self.id = self.project._new_script_id()

            data = {'id': self.id,
                    'label': self.label,
                    'program': None,
                    'filename': None,
                    'source_path': None,
                    'sources': [],
                    'user': self.project.user,
                    'added': time.time(),
                    'updated': -1,
                    'dependent_on': [],
                    'dependents': [],
                    'timelimit': -1,
                    'cores': 1,
                    'fail_if_parent_fails': True}

            self.project.db_scripts.insert(data)

            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
        else:
            raise Exception('Script already exists')

    def new_process(self, args):
        pass

    def _load(self):
        """
        Loads a job given its id.

        Returns true is loaded otherwise false.
        """
        script = self.project.db_scripts.find_one({'label': self.label})
        if script != None:
            self.id = script['id']

    def reset(self):
        self.project.db_scripts.update({'id': self.id},
                                       {'$set': {'program': None}})
        self.project.db_scripts.update({'id': self.id},
                                       {'$set': {'script': None}})
        self.project.db_scripts.update({'id': self.id},
                                       {'$set': {'sources': []}})
        self.project.db_scripts.update({'id': self.id},
                                       {'$set': {'dependent_on': []}})
        self.project.db_scripts.update({'id': self.id},
                                       {'$set': {'dependents': []}})

    def set_data(self, key, value):
        """
        Sets the value of a key.
        """
        self.project.db_scripts.update({'id': self.id},
                                       {'$set': {key: value}})

    def append_data(self, key, value):
        """
        Appends data to a list.
        """
        self.project.db_scripts.update({'id': self.id},
                                       {'$push': {key: value}})

    def set_source_path(self, path):
        self.set_data('source_path', os.path.abspath(path))

    def set_program(self, program):
        self.set_data('program', program)

    def set_script(self, script):
        print('set_script deprecated, use set_filename')
        self.set_filename(script)

    def set_filename(self, filename):
        self.set_data('filename', filename)

    def set_time_limit(self, timelimit):
        """
        Sets the time limit for which a process for this script can run
        for. Default is -1, which means it can run for an unlimited
        amount of time.
        """
        self.set_data('timelimit', timelimit)

    def set_cores_required(self, number_cores):
        """
        Sets the number of cores used by this script. Default is 1.
        This allows BPM to run multiple scripts/processes on multi-core
        machines.
        """
        self.set_data('cores', number_cores)

    @property
    def cores(self):
        return self.data.get('cores', 1)

    @property
    def on_hold(self):
        return self.data.get('on_hold', False)

    def set_hold_state(self, state):
        """
        Sets whether the script is allowed to run. If not it will stop the propagation
        of processes.
        """
        self.set_data('on_hold', state)

    def set_source(self, path, update_mode='copy'):
        print('set_source deprecated. Use add_source instead.')
        self.add_source(path, update_mode=update_mode)

    def has_source(self, source):
        for data_source in self.data['sources']:
            if data_source['path'] == source:
                return True
        return False

    def clear_sources(self):
        self.set_data('sources', [])

    def add_source(self, path, update_mode='copy'):
        self.append_data('sources', {'path': path,
                                     'update_mode': update_mode})

    def update_from_source(self):
        path = self.data['import_path']
        spath = path.split('/')
        module_name = os.path.splitext(spath.pop())[0]
        spath = '/'.join(spath)

        script_module = import_module('bpm_import_script_tmp', spath, module_name)

        source_path = self.data['source_path']

        self.set_program(script_module.run_program)
        self.set_filename(script_module.run_script)

        if hasattr(script_module, 'cores'):
            self.set_cores_required(script_module.cores)

        if hasattr(script_module, 'time_limit'):
            self.set_time_limit(script_module.time_limit)

        if hasattr(script_module, 'depends_on'):
            for dependency in script_module.depends_on:
                self.add_dependency(dependency)

        self.clear_sources()
        if hasattr(script_module, 'files'):
            for source_file in script_module.files:
                self.add_source(source_file)
        if self.has_source(script_module.run_script) == False:
            self.add_source(script_module.run_script)

        for source in self.data['sources']:
            if source is None:
                raise Exception('No source data setup')
            if source['update_mode'] == 'copy':
                from_path = self.project.process_path(source['path'], source_path)
                to_path = os.path.join(self.directory)
                print('Copying', from_path, to_path)
                if os.path.exists(from_path):
                    shutil.copy(from_path, to_path)
                else:
                    raise Exception('No update. Source file not found at %s.' % from_path)
            else:
                raise Exception('Unknown source update mode')

    def add_dependency(self, parent_script_label):
        for dependent in self.data['dependent_on']:
            if dependent == parent_script_label:
                print('Script already exists as a dependency')
                return 1
        self.append_data('dependent_on', parent_script_label)
        parent_script = self.project.script(parent_script_label)
        if parent_script is None:
            raise Exception('Parent script does not exist.')
        else:
            parent_script.add_dependent(self.label)

    def add_dependent(self, child_script_label):
        for dependent in self.data['dependents']:
            if dependent == child_script_label:
                print('Script already exists in parent')
                return 1
        self.append_data('dependents', child_script_label)

    def queue_dependent(self, dependent_script, parent_process):
        for dependent in self.data['dependents']:
            if dependent == dependent_script:
                child_script = self.project.script(dependent)
                child_script.run({}, parent_process.id)

    def queue_dependents(self, parent_process=None, status='pending'):
        for dependent in self.data['dependents']:
            child_script = self.project.script(dependent)
            child_script.run({}, parent_process.id, status=status)

    def find_existing_process_by_parent(self, parent_id):
        existing_process = self.project.db_processes.find_one(
            {'script': self.label,
             'parent': parent_id})
        if existing_process is not None:
            return self.project.process(existing_process['id'])
        return None

    def queue_process(self, params={}, parent_id=None):
        print('Deprecate script.queue_process(...), use script.run(...)')
        self.run(params=params, parent_id=parent_id)

    def spawn(self, params):
        pass

    def run(self, params={}, parent_id=None, status='pending'):
        if parent_id is None:
            process = None
            parent_process = None
        else:
            parent_process = self.project.process(parent_id)
            existing_process = self.project.db_processes.find_one(
                {'script': self.label,
                 'parent': parent_id})

            process = self.find_existing_process_by_parent(parent_id)

        if process is None:
            new_pid = self.project._new_process_id()
            if parent_process == None:
                root = new_pid
            else:
                root = parent_process.root.id
            process = {'id': new_pid,
                       'label': self.label,
                       'script': self.label,
                       'params': params,
                       'metadata': {},
                       'parent': parent_id,
                       'root': root,
                       'workspaces': {},
                       'status': status, 'message': '',
                       'started': -1, 'duration': -1,
                       'priority': 3,
                       'lock': False}
            self.project.db_processes.insert(process)
            process = self.project.process(new_pid)

            spath = self.path.split('/')
            module_name = os.path.splitext(spath.pop())[0]
            spath = '/'.join(spath)
            if 'bpm_import_script_tmp' in sys.modules:
                sys.modules.pop('bpm_import_script_tmp')
            script_module = import_module('bpm_import_script_tmp', spath, module_name)
            if hasattr(script_module, 'init'):
                process = script_module.init(process)

        else:
            process.queue()

        if parent_process is None:
            status = 'waiting'

        if status == 'waiting':
            self.queue_dependents(parent_process=process, status='waiting')

    def load_as_module(self):
        spath = self.path.split('/')
        module_name = os.path.splitext(spath.pop())[0]
        spath = '/'.join(spath)
        unique_name = 'bpm_import_script_' + self.label
        if unique_name in sys.modules:
            sys.modules.pop(unique_name)
        return import_module(unique_name, spath, module_name)

