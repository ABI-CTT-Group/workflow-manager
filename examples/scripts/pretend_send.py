import argparse
import os
import shutil

import workflow_manager as wm

script_id = 'pretend_send'
run_program = 'python3'
run_script = 'pretend_send.py'
depends_on = ['pretend_mechanics1', 'pretend_mechanics2']


def run(process):
    source_workspace = process.parent.get_workspace('pretend_mechanics')
    send_dir = process.root.params.get('send_dir')

    source = source_workspace.path()

    send(source, send_dir)

    process.completed()


def send(source, send_dir):
    if not os.path.isdir(send_dir):
        os.makedirs(send_dir)
    files = os.listdir(source)
    for file in files:
        path = os.path.join(source, file)
        shutil.copy(path, send_dir)


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
            send(source, dest)
    except:
        run(wm.get_project_process())

    # run(wm.get_project_process())

    # source = "../tmp/"
    # dest = "../tmp1/"
    # send(source, dest)
