import os

import workflow_manager as wm

if __name__ == '__main__':
    project_name= "test_project"

    P = wm.Project(project_name)
    script = P.script('pretend_import')
    script_input_arguments = {'path': 'data/pretend_data.txt', 'send_dir': os.path.join(P.root_dir, 'results')}
    script.run(script_input_arguments)

    wm.project.start_process_monitor(project_name, minutes_alive=3, sleep_time=3, total_cores=8)