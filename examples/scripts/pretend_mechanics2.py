script_id = 'pretend_mechanics2'
run_program = 'python3'
run_script = 'pretend_mechanics2.py'
files = ['pretend_module.py']
depends_on = ['pretend_fit']


def run(process):
    import time
    source_workspace = process.parent.get_workspace('pretend_fit')
    dest_workspace = process.get_workspace('pretend_mechanics', True)

    print("Source workspace:")
    print("    path:" + str(source_workspace.path()))
    print("Destination workspace:")
    print("    path:" + str(dest_workspace.path()))

    fit_data = int(source_workspace.open_file('mesh.txt').readline())
    fp = dest_workspace.open_file('solution2.txt', 'w')
    fp.write(str(fit_data + 10))
    fp.close()
    time.sleep(2)
    process.completed()


if __name__ == "__main__":
    import workflow_manager as wm

    run(wm.get_project_process())
