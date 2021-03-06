script_id = 'pretend_import'
run_program = 'python3'
run_script = 'pretend_import.py'

import os


def init(process):
    path = process.params.get('path')
    process.set_param('path', os.path.abspath(path))
    return process


def run(process):
    path = process.params.get('path')
    workspace = process.get_workspace('pretend_import', True)

    print("Workspace:")
    print("    path:" + str(workspace.path()))

    if os.path.isdir(path):
        files = os.listdir(path)
        paths = list()
        for file in files:
            paths.append(os.path.join(path, file))
        print("list of files:" + str(paths))
        status, message = workspace.copy_files(paths)
    else:
        status, message = workspace.copy_file(path)

    process.completed(status, message)


if __name__ == "__main__":
    import workflow_manager as wm

    run(wm.get_project_process())
