script_id = 'mechanics2'
run_program = 'python3'
run_script = 'pretend_mechanics2.py'
files = ['pretend_module.py']
depends_on = ['fit']

def run(process):
    import time
    fit_workspace = process.parent.get_workspace('fit')
    fem_workspace = process.get_workspace('mechanics', True)
    fit_data = int(fit_workspace.open_file('mesh.txt').readline())
    fp = fem_workspace.open_file('solution.txt', 'w')
    fp.write(str(fit_data + 10))
    fp.close()
    time.sleep(2)
    process.completed()


if __name__ == "__main__":
    import workflow_manager as wm
    run(wm.get_project_process())
