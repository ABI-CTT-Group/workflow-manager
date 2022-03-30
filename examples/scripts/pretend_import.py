import argparse
import os
import shutil

import workflow_manager as wm

script_id = 'pretend_import'
run_program = 'python3'
run_script = 'pretend_import.py'

parser = argparse.ArgumentParser(description='Import Scans')
parser.add_argument('--workflow',
                    choices=('True', 'False'),
                    default='True',
                    help='Run in workflow')
parser.add_argument('--source',
                    default=None,
                    help='Source dir or file')
parser.add_argument('--dest',
                    default=None,
                    help='Destination folder')


def init(process):
    path = process.params.get('path')
    process.set_param('path', os.path.abspath(path))
    return process


def run(process):
    path = process.params.get('path')
    workspace = process.get_workspace('pretend_import', True)

    print("Workspace:")
    print("    path:" + str(workspace.path()))

    status, message = import_scans(path, workspace.path())

    process.completed(status, message)


def import_scans(source, dest):
    print("Source:" + str(source))
    print("Destination:" + str(dest))

    if os.path.isdir(source):
        files = os.listdir(source)
        paths = list()
        for file in files:
            path = os.path.join(source, file)
            if os.path.exists(path):
                paths.append(os.path.join(source, file))
            else:
                return False, 'Source file not found %s' % path

        print("list of files:" + str(paths))

        for path in paths:
            shutil.copy(path, dest)
    else:
        shutil.copy(source, dest)

    return True, ''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import Scans')
    parser.add_argument('--workflow',
                        choices=('True', 'False'),
                        default='True',
                        help='Run in workflow')
    parser.add_argument('--source',
                        default=None,
                        help='Source dir or file')
    parser.add_argument('--dest',
                        default=None,
                        help='Destination folder')
    try:
        args = parser.parse_args()
        run_workflow = args.workflow == 'True'
        print(str(args))
        if run_workflow:
            run(wm.get_project_process())
        else:
            source = args.source
            dest = args.dest
            import_scans(source, dest)
    except:
        run(wm.get_project_process())

    # source = "../data/pretend_data.txt"
    # dest = "../tmp/"
    # import_scans(source, dest)

    # run(wm.get_project_process())
