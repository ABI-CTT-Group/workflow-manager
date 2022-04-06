import sys
import os
import workflow_manager

if __name__ == '__main__':
    if len(sys.argv) < 0:
        raise Exception('InputError.')
    path = sys.argv[1]
    project_name = sys.argv[2]

    P = workflow_manager.Project(project_name)
    script = P.script('pretend_import')
    script_input_arguments = {'path': path, 'send_dir': os.getenv('RESULTS')}
    script.run(script_input_arguments)