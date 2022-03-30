import argparse
import os
import time

import workflow_manager as wm

script_id = 'pretend_mechanics2'
run_program = 'python3'
run_script = 'pretend_mechanics2.py'
files = ['pretend_module.py']
depends_on = ['pretend_fit']


def run(process):
    source_workspace = process.parent.get_workspace('pretend_fit')
    dest_workspace = process.get_workspace('pretend_mechanics', True)

    print("Source workspace:")
    print("    path:" + str(source_workspace.path()))
    print("Destination workspace:")
    print("    path:" + str(dest_workspace.path()))

    source = os.path.join(source_workspace.path(), "mesh.txt")
    dest = os.path.join(dest_workspace.path(), "solution2.txt")

    mechanics(source, dest)
    process.completed()

def mechanics(source, dest):
    fp = open(source)
    fit_data = int(fp.readline())

    fp = open(dest, 'w')
    fp.write(str(fit_data + 10))
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
            mechanics(source, dest)
    except:
        run(wm.get_project_process())

    # run(wm.get_project_process())

    # source = "../tmp/mesh.txt"
    # dest = "../tmp/solution2.txt"
    # mechanics(source, dest)
