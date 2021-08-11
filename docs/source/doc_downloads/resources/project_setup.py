import os
import sys

import workflow_manager as wm

if __name__ == '__main__':
    project_name = sys.argv[1]
    project_root = sys.argv[2]

    os.makedirs(project_root)
    P = wm.create_project(project_name, root_dir=project_root)

    P.import_script('./scripts/script1.py')
    P.import_script('./scripts/script2.py')
    P.import_script('./scripts/script3.py')

    script = P.script('script1')
    script_input_arguments = {'path': 'relativePathToInputData/pretend_data.txt', 'send_dir': os.getenv('RESULTS')}
    script.run(script_input_arguments)

    wm.project.start_process_monitor(project_name, minutes_alive=999, sleep_time=3, total_cores=8)