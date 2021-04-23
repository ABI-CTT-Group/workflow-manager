import workflow_manager as wm

if __name__ == '__main__':
    project_name = 'test_project'
    P = wm.Project(project_name)

    print("Scripts:")
    P.list_scripts()
    print("Processes and their status:")
    P.list_processes()