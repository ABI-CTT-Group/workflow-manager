script_id = 'fit'
run_program = 'python3'
run_script = 'pretend_fit.py'
depends_on = ['segment']

def run(process):
    segment_wksp = process.parent.get_workspace('segment')
    fit_wksp = process.get_workspace('fit', True)
    segment_data = int(segment_wksp.open_file('pointcloud.txt').readline())
    fp = fit_wksp.open_file('mesh.txt', 'w')
    fp.write(str(segment_data + 18))
    fp.close()
    process.completed()


if __name__ == "__main__":
    import workflow_manager as wm
    run(wm.get_project_process())
