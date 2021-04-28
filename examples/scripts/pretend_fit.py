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

    segment_data = int(source_workspace.open_file('pointcloud.txt').readline())
    fp = dest_workspace.open_file('mesh.txt', 'w')
    fp.write(str(segment_data + 18))
    fp.close()
    process.completed()


if __name__ == "__main__":
    import workflow_manager as wm

    run(wm.get_project_process())
