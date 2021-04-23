import os
import time
import datetime
import pymongo
import psutil
import subprocess

from workflow_manager.utils import pretty_time

COL_RED = '\033[1;91m'
COL_BLUE = '\033[0;94m'
COL_BLUEBR = '\033[1;34m'
COL_BLUEBG = '\033[44m'
COL_CYAN = '\033[96m'
COL_GREEN = '\033[1;92m'
COL_ORANGE = '\033[33m'
COL_YELLOW = '\033[33m'
END_COL = '\033[0m'


class Process(object):
    def __init__(self, project, id):
        self.project = project
        if isinstance(id, str):
            id = int(id)
        self.id = id

    def __str__(self):
        data = self.data

        col1 = ''
        if self.status == 'Success':
            col1 = COL_GREEN
        elif self.status == 'Failure':
            if self.message == 'Parent failed':
                col1 = COL_ORANGE
            else:
                col1 = COL_RED
        elif self.status == 'processing':
            col1 = COL_BLUEBG
        elif self.status == 'pending':
            col1 = COL_BLUEBR
        elif self.status == 'waiting':
            col1 = COL_BLUE
        col2 = END_COL

        ancestors_str = 'root'
        if self.parent is not None:
            ancestors_str = '%d %d' % (self.parent.id, self.root.id)

        label_str = '{:<24s}'.format(self.label)
        string = '%3d %s%s%s %7s' % (self.id, col1, label_str, col2, ancestors_str)
        string += ' %5s' % (pretty_time(self.duration))
        wksp = ''
        workspaces = self.data['workspaces']
        for wk in workspaces.keys():
            wksp += ' %s: %d,' % (wk, workspaces[wk])
        wksp = wksp[:-1]
        string += ' %s' % ('{:<16s}'.format(wksp))
        string += ' %s' % data['message']
        return string

    @property
    def data(self):
        return self.project.db_processes.find_one({'id': self.id})

    @property
    def params(self):
        return self.data['params']

    @property
    def metadata(self):
        return self.data['metadata']

    @property
    def label(self):
        """
        Returns the label of the script for this process
        """
        return self.data['label']

    @property
    def process_dir(self):
        path = os.path.join(self.project.processes_dir, str(self.id))
        if not os.path.exists(path):
            os.makedirs(path)
        return path + '/'

    @property
    def script(self):
        """
        Returns the script for this process
        """
        return self.project.script(self.data['script'])

    @property
    def cores(self):
        """
        Returns the number or cores required by this script/process
        """
        return self.script.cores


    @property
    def parent_process(self):
        print('Deprecated, use process.parent instead.')
        return self.parent

    @property
    def parent(self):
        """
        Returns the parent process for this process, i.e., the process
        that spawned this process.

        This can strung together:
        `parent_process = process.parent.parent.parent`
        """
        if self.data['parent'] is None:
            return None
        return self.project.process(self.data['parent'])

    @property
    def root(self):
        """
        Returns the root process for this sequence of processes, i.e.,
        the original process that spawned this sequence process.
        """
        return self.project.process(self.data['root'])

    @property
    def status(self):
        """
        Returns the status this process
        """
        return str(self.data['status'])

    @property
    def message(self):
        """
        Returns the message for this process
        """
        return self.data['message']

    @property
    def duration(self, as_str=False):
        if self.status == 'processing':
            dt = time.time() - self.data['started']
        elif self.data['duration'] == -1:
            return 0
        else:
            dt = self.data['duration']
        return dt

    @property
    def started(self):
        return str(self.data['started'])

    def set_data(self, key, value):
        """
        Sets the value of a key.
        """
        self.project.db_processes.update({'id': self.id},
                                         {'$set': {key: value}})

    def set_param(self, key, value):
        params = self.params
        params[key] = value
        self.set_data('params', params)

    def has_metadata(self):
        return 'metadata' in self.data.keys()

    def clear_metadata(self):
        self.set_data('metadata', {})

    def set_metadata(self, key, value):
        metadata = self.metadata
        metadata[key] = value
        self.set_data('metadata', metadata)

    def append_data(self, key, value):
        """
        Appends data to a list.
        """
        self.project.db_processes.update({'id': self.id},
                                         {'$push': {key: value}})

    def open_logfile(self, logdatetime, mode='r'):
        filename = logdatetime.strftime('%Y%m%d%H%M%S') + '.log'
        path = os.path.join(self.process_dir, filename)
        return open(path, mode)

    def open_latest_log(self):
        filenames = self.get_list_of_logs()
        if len(filenames) > 0:
            path = os.path.join(self.process_dir, filenames[0])
            return open(path, 'r')
        else:
            return None

    def get_list_of_logs(self):
        logtxt = False
        allfilenames = os.listdir(self.process_dir)
        filenames = []
        for filename in allfilenames:
            if filename[-4:] == '.log':
                filenames.append(filename)
            elif filename == 'log.txt':
                logtxt = True
        filenames.sort()
        filenames.reverse()
        if logtxt:
            filenames.append('log.txt')
        return filenames

    def purge_logs(self, N=3):
        filenames = self.get_list_of_logs()
        if len(filenames) > N:
            for filename in filenames[N:]:
                os.remove(os.path.join(self.process_dir, filename))

    def get_decendents(self, label=None):
        processes = []
        search_dict = {}
        search_dict['parent'] = self.id
        if label is not None:
            search_dict['label'] = label

        for cursor in self.project.db_processes.find(search_dict, limit=0).sort('id', pymongo.DESCENDING):
            processes.append(Process(self.project, cursor['id']))

        return processes

    def get_ancestor(self, gen=None, label=None, id=None):
        """
        This return an ancestor of a process that matches the given
        generation, label, or id.

        ancestor = process.get_ancestor(gen=2) will return the ancestor
        two generations back, or None if none is found.

        ancestor = process.get_ancestor(id=63) will return the ancestor
        with an id of 63, or None if none is found.

        ancestor = process.get_ancestor(label='fit') will return the
        ancestor with the label "fit", or None if none is found.

        This function is a convinient wrapper to:
            process.get_ancestor_by_generation(gen)
            process.get_ancestor_by_id(id)
            process.get_ancestor_by_label(label)
        """
        if gen is not None:
            return self.get_ancestor_by_generation(gen)
        elif label is not None:
            return self.get_ancestor_by_label(label)
        elif id is not None:
            return self.get_ancestor_by_id(id)
        return None

    def get_ancestor_by_generation(self, gen):
        """
        This return an ancestor of a process that matches the given
        generation.

        ancestor = process.get_ancestor(gen=2) will return the ancestor
        two generations back, or None if none is found.
        """
        process = self
        for i in range(gen):
            process = process.parent
            if process is None:
                return None
        return process

    def get_ancestor_by_id(self, id):
        """
        This return an ancestor of a process that matches the given id.

        ancestor = process.get_ancestor(id=63) will return the ancestor
        with an id of 63, or None if none is found.
        """
        process = self
        while process.id != id:
            process = process.parent
            if process is None:
                return None
            elif process.id == id:
                return process
        return None

    def get_ancestor_by_label(self, label):
        """
        This return an ancestor of a process that matches the given
        label.

        ancestor = process.get_ancestor(label='fit') will return the
        ancestor with the label "fit", or None if none is found.
        """
        process = self
        while process.label != label:
            process = process.parent
            if process is None:
                return None
            elif process.label == label:
                return process
        return None

    def start(self):
        script = self.project.script(self.label)
        command = [script.data['program']]
        command.append('%s' % script.path)
        command.append('%s' % self.project.name)
        command.append('%s' % self.id)

        logdatetime = datetime.datetime.now()

        self.purge_logs(N=3)
        logfile = self.open_logfile(logdatetime, mode='w')
        logfile.write('\n\n\n')
        logfile.write('#############################################\n')
        logfile.write('%s - %s\n' % (
            logdatetime.strftime("%Y%m%d %H:%M:%S"),
            self.label))
        logfile.write('Process Command: %s\n' % (' '.join(command)))
        logfile.write('#############################################\n')

        start_process = True
        if script.data['fail_if_parent_fails']:
            if self.parent != None:
                if self.parent.status == 'Failure':
                    start_process = False
                    self.set_data('pid', -1)
                    self.set_data('started', time.time())
                    self.completed(False, 'Parent failed')

        if script.on_hold:
            start_process = False
            self.set_data('pid', -1)
            self.set_data('started', time.time())
            self.completed(False, 'Script on hold')

        if start_process:
            proc = subprocess.Popen(command, stdout=logfile, stderr=logfile,
                                    cwd=self.project.scripts_dir)
            self.set_data('pid', proc.pid)
            self.set_data('started', time.time())
            self.set_data('status', 'processing')
            self.set_data('message', '')

    def queue(self, params=None, propagate=True):
        if params is not None:
            if self.data['status'] not in ['processing']:
                for key in params.keys():
                    self.set_param(key, params[key])
            else:
                print('Warning: process already processing, actions not set')

        if self.data['status'] not in ['pending', 'processing']:
            self.set_data('status', 'pending')
            self.set_data('propagate', propagate)
            msg = self.data.get('message')
            self.set_data('message', '[' + msg + ']')

    def kill(self):
        if self.data['status'] == 'processing':
            pid = self.data.get('pid')
            if psutil.pid_exists(pid):
                os.kill(pid, 9)
                # ~ if psutil.pid_exists(pid):
                #~ os.waitpid(pid, 0)
            self.completed(False, 'Killed')
        elif self.data['status'] == 'pending':
            self.completed(False, 'Killed')

    def progress(self, progress):
        self.set_data('message', progress)

    def completed(self, status=True, message='', dt=None):
        status_string = 'Success' if status else 'Failure'
        self.set_data('status', status_string)
        self.set_data('message', message)

        if dt != None:
            self.set_data('duration', dt)
        elif self.data['started'] == -1:
            self.set_data('duration', 0)
        else:
            self.set_data('duration', time.time() - self.data['started'])

        if status:
            print(COL_GREEN + self.status + END_COL, pretty_time(self.duration), self.message)
        else:
            print(COL_RED + self.status + END_COL, pretty_time(self.duration), self.message)
        if self.data.get('propagate', True):
            script = self.project.script(self.data['script'])
            script.queue_dependents(self)

    def check_status(self):

        if psutil.pid_exists(self.data['pid']):
            timelimit = self.script.data['timelimit']
            proc = psutil.Process(self.data['pid'])
            # if process is defunct, kill job and update status

            if len(proc.cmdline()) == 0 and self.script.data['program'] in proc.name():
                os.kill(proc.pid, 9)
                if psutil.pid_exists(self.data['pid']):
                    os.waitpid(proc.pid, 0)
                self.completed(False, 'Process defunct')

            elif timelimit > -1:
                if self.status == 'processing':
                    if time.time() - self.data['started'] > timelimit:
                        print('Killing due to timelimit')
                        pid = self.data['pid']
                        if psutil.pid_exists(pid):
                            os.kill(pid, 9)
                        self.completed(False, 'Time limit exceeded')

        else:
            if self.data['status'] == 'processing':
                self.completed(False, 'Process lost')

    def queue_dependent(self, dependent_script):
        script = self.project.script(self.data['script'])
        script.queue_dependent(dependent_script, self)

    def workspace(self, label, create=False):
        return self.get_workspace(label, create)

    def get_workspace(self, label, create=False):
        """
        Returns a workspace with a given label that is associated with
        the process.

        If the workspace does not exist, it will create
        and return a new workspace if ``create=True`` otherwise it will
        return None.
        """
        workspace_id = self.data['workspaces'].get(label)
        if workspace_id is None:
            if create:
                workspace = self.project.new_workspace(label)
                workspace.add_data({'process': self.id})
                self.project.db_processes.update({'id': self.id},
                                                 {'$set': {'workspaces.' + label: workspace.id}})
                return workspace
        else:
            workspace = self.project.workspace(workspace_id)
            return workspace
        return None

    def get_workspaces(self):
        return [self.project.workspace(wid[1]) for wid in self.data['workspaces'].iteritems()]

    def log(self, num_lines=None):
        log_separator = '#############################################\n'
        fp = self.open_latest_log()
        lines = []
        if num_lines is None:
            state = 0
            for line in self.reverse_file(fp):
                if line == log_separator:
                    state += 1
                lines.append(line)
                if state == 2:
                    break
        else:
            for i, line in enumerate(self.reverse_file(fp)):
                lines.append(line)
                if i > num_lines:
                    break

        fp.close()
        lines.reverse()
        for line in lines:
            print(line.rstrip())

    def reverse_file(self, myfile):
        """
        Iterates the lines of a file, but in reverse order
        """
        myfile.seek(0)
        offsets = self._getLineOffsets(myfile)
        myfile.seek(0)
        offsets.reverse()
        for i in offsets:
            myfile.seek(i + 1)
            yield myfile.readline()

    def _getLineOffsets(self, myfile):
        """
        Return a list of offsets where newlines are located.
        """
        offsets = [-1]
        i = 0
        while True:
            byte = myfile.read(1)
            if not byte:
                break
            elif byte == '\n':
                offsets.append(i)
            i += 1
        return offsets


