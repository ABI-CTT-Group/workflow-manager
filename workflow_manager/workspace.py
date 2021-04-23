import datetime
import hashlib
import os
import shutil
import time
import zipfile


class Workspace(object):
    """
    A workspace is where data is stored. These are typically stored in
    path_to_project_dir/workspaces.

    Workspaces are typically created through processes which means they
    are associated with the process but you can create orphan workspaces.
    In other words, they aren't associated with a process. An orphan
    workspace can be created through the project using the
    Project.new_workspace(label=None) command.
    """

    def __init__(self, project, workspace_id=None, label=None):
        self.project = project
        self._path_ = None
        if workspace_id is None:
            self._new(label=label)
        else:
            self._load(workspace_id)

    @property
    def data(self):
        """
        Returns a dictionary of the data associated with the workspace.
        """
        return self.project.db_workspaces.find_one({'id': self.id})

    def _new(self, label=None):
        """
        Creates a new job

        Return job_id
        """
        if not os.path.exists(self.project.workspaces_dir):
            raise Exception('Workspaces directory does not exist')

        self.id = self.project._new_workspace_id()

        workspace_dir = '%06d' % self.id
        self._path_ = os.path.join(self.project.workspaces_dir, workspace_dir) + '/'
        os.makedirs(self._path_)

        data = {'id': self.id,
                'user': self.project.user,
                'path': workspace_dir,
                'status': 'active',
                'created': time.time()}

        if label is not None:
            data['label'] = label

        self.project.db_workspaces.insert(data)

    def _load(self, id):
        """
        Loads a job given its id.

        Returns true is loaded otherwise false.
        """
        self.id = id
        data = self.project.db_workspaces.find_one({'id': self.id})
        self._path_ = os.path.join(self.project.workspaces_dir, self.data['path']) + '/'

    def path(self, *args):
        if len(args) == 0:
            return str(self._path_)
        else:
            return str(os.path.join(self._path_, *args))

    def list(self):
        print(os.listdir(self.path()))

    def set_data(self, key, value):
        """
        Sets the value of a key.
        """
        self.project.db_workspaces.update({'id': self.id},
                                          {'$set': {key: value}})

    def append_data(self, key, value):
        """
        Appends data to a list.
        """
        self.project.db_workspaces.update({'id': self.id},
                                          {'$push': {key: value}})

    def add_data(self, data):
        """
        Adds data as a dictionary.

        Example:
            workspace.add_data({'elements':[1,3,5]})
        """
        self.project.db_workspaces.update({'id': self.id}, {'$set': data})

    def delete_folder(self):
        self.clear_directory_contents(self.path())
        shutil.rmtree(self.path())

    def clear(self):
        protected_dirs = ['.versions']
        self.clear_directory_contents(self.path(), protected_dirs=protected_dirs)

    def clear_directory_contents(self, directory_path, protected_dirs=[]):
        items = os.listdir(directory_path)
        for item in items:
            filepath = os.path.join(directory_path, item)
            if os.path.isfile(filepath):
                os.unlink(filepath)
            elif os.path.isdir(filepath):
                if item not in protected_dirs:
                    shutil.rmtree(filepath)

    def copy_directory_contents(self, source_dir, dest_dir):
        items = os.listdir(source_dir)
        for item in items:
            filepath = os.path.join(source_dir, item)
            if os.path.isfile(filepath):
                shutil.copy(filepath, os.path.join(dest_dir, item))
            elif os.path.isdir(filepath):
                if item[0] != '.':
                    shutil.copytree(filepath, os.path.join(dest_dir, item))

    def create_version(self, label=None, overwrite=False):
        # Check the versions directory exists
        versions_dir = self.path('.versions')
        if not os.path.exists(versions_dir):
            os.mkdir(versions_dir)

        # Init a directory for this version
        if label == None:
            label = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        version_dir = os.path.join(versions_dir, label)
        if os.path.exists(version_dir):
            if overwrite:
                self.clear_directory_contents(version_dir)
            else:
                print('Warning: No version created since already exists (use overwrite=True)')
        else:
            os.mkdir(version_dir)

        self.copy_directory_contents(self.path(), version_dir)

    def compare_versions(self, label=None, label2=None):
        ### TODO: if label == None, use most recent version
        ### TODO: if label2 == None use current workspace files

        # Check version directory exists
        version_dir = self.path('.versions', label)
        if not os.path.exists(version_dir):
            raise Exception('Version does not exist')

        # get files in workspace
        items = os.listdir(self.path())

        # get max filename length
        maxlen = 0
        for item in items:
            lenitem = len(item)
            if lenitem > maxlen:
                maxlen = lenitem
        strformat = '%%-%ds : %%s' % (maxlen)

        # compare files
        any_mismatch = False
        for item in items:
            if item != '.versions':
                wksp_file = self.path(item)
                vers_file = version_dir(item)
                if os.path.exists(vers_file):
                    wksp_md5 = self.md5sum(wksp_file)
                    vers_md5 = self.md5sum(vers_file)
                    if wksp_md5 != vers_md5:
                        print(strformat % (item, 'MD5sum mismatch'))
                        any_mismatch = True
                else:
                    print(strformat % (item, 'Missing'))
                    any_mismatch = True
        if not any_mismatch:
            print('Versions are identical')

    def md5sum(self, filepath):
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def open_file(self, filename, mode='r'):
        """
        Opens a file in the workspace and returns the file pointer object.
        """
        return open(self.path(filename), mode)

    def delete(self, filepath):
        fullpath = self.path(filepath)
        if os.path.exists(fullpath):
            os.unlink(fullpath)

    def copy_file(self, filepath):
        return self.copy_files([filepath])

    def copy_files(self, filepaths):
        """
        Copies files into the workspace.
        """
        for filepath in filepaths:
            filepath = self.project.process_path(filepath)
            # print 'Workspace %d copying %s' % (self.id, filepath)
            # Copy data file
            if os.path.exists(filepath):
                shutil.copy(filepath, self.path())
            else:
                return False, 'Source file not found %s' % filepath
        return True, ''

    def extract_zipfile(self, filepath):
        """
        Extracts a zip file into the workspace.
        """
        filepath = self.project.process_path(filepath)
        # Check zip file exists
        if os.path.exists(filepath):
            zip_obj = zipfile.ZipFile(filepath)
        else:
            return False, 'Zip file not found'
        # Extract zip file to workspace
        zip_obj.extractall(path=self.path())
        zip_obj.close()
        return True, ''


