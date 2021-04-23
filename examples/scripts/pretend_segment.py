script_id = 'segment'
run_program = 'python3'
run_script = 'pretend_segment.py'
files = ['pretend_segment.py']
depends_on = ['import']
cores = 2
time_limit = 4

def run(process):
    import time
    scan_workspace = process.parent.get_workspace('scan')
    segment_workspace = process.get_workspace('segment', True)
    source_data = int(scan_workspace.open_file('pretend_data.txt').readline())
    fp = segment_workspace.open_file('pointcloud.txt', 'w')
    fp.write(str(2 * source_data))
    fp.close()
    if process.id == 7:
        print('SLEEPING FOR 10s')
        time.sleep(10)
    else:
        time.sleep(3)
    process.completed()


if __name__ == "__main__":
    import workflow_manager as wm
    run(wm.get_project_process())
