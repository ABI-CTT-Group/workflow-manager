import argparse
import os
import time

import workflow_manager as wm

script_id = 'pretend_segment'
run_program = 'python3'
run_script = 'pretend_segment.py'
files = ['pretend_segment.py']
depends_on = ['pretend_import']
cores = 2
time_limit = 4


def run(process):
    source_workspace = process.parent.get_workspace('pretend_import')
    dest_workspace = process.get_workspace('pretend_segment', True)

    print("Source workspace:")
    print("    path:" + str(source_workspace.path()))
    print("Destination workspace:")
    print("    path:" + str(dest_workspace.path()))

    source = os.path.join(source_workspace.path(), "pretend_data.txt")
    dest = os.path.join(dest_workspace.path(), "pointcloud.txt")
    segment(source, dest)
    
    process.completed()


def segment(source, dest):
    fp = open(dest, 'w')
    fp.write(str(10))
    fp.close()
    time.sleep(3)
    

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
            segment(source, dest)
    except:
        run(wm.get_project_process())

    # run(wm.get_project_process())

    # source = "../tmp/pretend_data.txt"
    # dest = "../tmp/pointcloud.txt"
    # segment(source, dest)
    
    
    
