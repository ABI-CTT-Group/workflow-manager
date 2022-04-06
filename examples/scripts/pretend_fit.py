import argparse
import os

import workflow_manager as wm

script_id = 'pretend_fit'
run_program = 'python3'
run_script = 'pretend_fit.py'
depends_on = ['pretend_segment']


def run(process):
    source_workspace = process.parent.get_workspace('pretend_segment')
    dest_workspace = process.get_workspace('pretend_fit', True)

    print("Source workspace:")
    print("    path:" + str(source_workspace.path()))
    print("Destination workspace:")
    print("    path:" + str(dest_workspace.path()))

    source = os.path.join(source_workspace.path(), "pointcloud.txt")
    dest = os.path.join(dest_workspace.path(), "mesh.txt")

    fit(source, dest)
    process.completed()


def fit(source, dest):
    fp = open(source)
    segment_data = int(fp.readline())

    fp = open(dest, 'w')
    fp.write(str(segment_data + 18))
    fp.close()


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
            fit(source, dest)
    except:
        run(wm.get_project_process())

    # run(wm.get_project_process())

    # source = "../tmp/pointcloud.txt"
    # dest = "../tmp/mesh.txt"
    # fit(source, dest)