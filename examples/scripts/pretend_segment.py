script_id = 'pretend_segment'
run_program = 'python3'
run_script = 'pretend_segment.py'
files = ['pretend_segment.py']
depends_on = ['pretend_import']
cores = 2
time_limit = 4


def run(process):
    import time
    source_workspace = process.parent.get_workspace('pretend_import')
    dest_workspace = process.get_workspace('pretend_segment', True)

    print("Source workspace:")
    print("    path:" + str(source_workspace.path()))
    print("Destination workspace:")
    print("    path:" + str(dest_workspace.path()))

    fp = dest_workspace.open_file('pointcloud.txt', 'w')
    fp.write(str(10))
    fp.close()
    time.sleep(3)
    process.completed()


if __name__ == "__main__":
    import workflow_manager as wm

    run(wm.get_project_process())
