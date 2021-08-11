import os
import shutil

script_id = 'pretend_send'
run_program = 'python3'
run_script = 'pretend_send.py'
depends_on = ['pretend_mechanics1', 'pretend_mechanics2']

def run(process):
    source_workspace = process.parent.get_workspace('pretend_mechanics')

    send_dir = process.root.params.get('send_dir')
    if not os.path.isdir(send_dir):
        os.makedirs(send_dir)

    files = os.listdir(source_workspace.path())
    for file in files:
        path = os.path.join(source_workspace.path(), file)
        shutil.copy(path, send_dir)

    process.completed()


if __name__ == "__main__":
    import workflow_manager as wm

    run(wm.get_project_process())
