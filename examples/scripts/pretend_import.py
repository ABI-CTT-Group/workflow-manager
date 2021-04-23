script_id = 'import'
run_program = 'python3'
run_script = 'pretend_import.py'

def init(process):
    import os
    path = process.params.get('path')
    process.set_param('path', os.path.abspath(path))
    return process

def run(process):
    filepath = process.params.get('path')
    workspace = process.get_workspace('scan', True)
    status, message = workspace.copy_file(filepath)
    process.completed(status, message)


if __name__ == "__main__":
    import workflow_manager as wm
    run(wm.get_project_process())
