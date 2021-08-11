"""
Enable Pytest for your Pycharm project﻿
https://www.jetbrains.com/help/pycharm/pytest.html#enable-pytest
"""
import pytest

import pymongo
import os
import shutil

import workflow_manager as wm

pytest.project_name = "project_temp"
pytest.project_root = './tmp/project_temp'
pytest.conn = None


def delete_project_from_db(project_name, db_connection):
    if project_name in db_connection.list_database_names():
        print('DROP %s database' % pytest.project_name)
        db_connection.drop_database(pytest.project_name)


def delete_project_root(project_root):
    if os.path.exists(project_root):
        print('DELETE %s directory' % pytest.project_root)
        shutil.rmtree(pytest.project_root)


@pytest.fixture(scope="session", autouse=True)
def connect_db():
    pytest.conn = pymongo.MongoClient('localhost', 27017)


@pytest.fixture(scope="session", autouse=True)
def create_project():
    delete_project_from_db(pytest.project_name, pytest.conn)
    delete_project_root(pytest.project_root)

    P = wm.create_project(pytest.project_name, root_dir=pytest.project_root)

    P.import_script('../examples/scripts/pretend_import.py')
    P.import_script('../examples/scripts/pretend_segment.py')
    P.import_script('../examples/scripts/pretend_fit.py')
    P.import_script('../examples/scripts/pretend_mechanics1.py')
    P.import_script('../examples/scripts/pretend_mechanics2.py')
    P.import_script('../examples/scripts/pretend_send.py')


@pytest.fixture(scope="session", autouse=True)
def run_project():
    P = wm.Project(pytest.project_name)
    script = P.script('pretend_import')
    script_input_arguments = {'path': '../examples/data/pretend_data.txt',
                              'send_dir': os.path.join(P.root_dir, 'results')}
    script.run(script_input_arguments)

    print("Setting up and running the project...")
    print("Tests will be run in 1 minute!")
    wm.project.start_process_monitor(pytest.project_name, minutes_alive=1, sleep_time=1, total_cores=8)


@pytest.fixture(scope="session", autouse=True)
def delete_project_after():
    yield

    delete_project_from_db(pytest.project_name, pytest.conn)
    delete_project_root(pytest.project_root)


def test_pretend_import():
    """
    given a project with the pretend_import script imported as the 1st script,
    when I run the project with the pretend_data.txt as input,
    should see pretend_data.txt passed into the 1st workspace
    :return:
    :rtype:
    """

    path = os.path.join(pytest.project_root, 'workspaces', '000001', 'pretend_data.txt')

    assert os.path.isfile(path)


def test_pretend_segment():
    """
    given a project with the pretend_segment script imported as the 2nd script (depends on pretend_import),
    when I run the project,
    should see pointcloud.txt in the 2nd workspace
    """

    path = os.path.join(pytest.project_root, 'workspaces', '000002', 'pointcloud.txt')

    assert os.path.isfile(path)


def test_pretend_fit():
    """
    given a project with the pretend_fit script imported as the 3rd script (depends on pretend_segment),
    when I run the project,
    should see mesh.txt in the 3rd workspace
    :return:
    :rtype:
    """

    path = os.path.join(pytest.project_root, 'workspaces', '000003', 'mesh.txt')

    assert os.path.isfile(path)


def test_pretend_mechanics():
    """
    given a project with the pretend_mechanics1 and pretend_mechanics2 scripts imported as the 4th and 5th scripts
    (both depend on pretend_fit and will be run right after the completion of pretend_fit in a random order),
    when I run the project,
    should see solution1.txt in the 4th/5th workspace and solution2.txt in the 4th/5th workspace.
    """

    workspace_a_path = os.path.join(pytest.project_root, 'workspaces', '000004')
    workspace_b_path = os.path.join(pytest.project_root, 'workspaces', '000005')
    workspace_a_files = os.listdir(workspace_a_path)
    workspace_b_files = os.listdir(workspace_b_path)
    files = workspace_a_files + workspace_b_files

    assert ('solution1.txt' in files) and ('solution2.txt' in files)


def test_pretend_send():
    """
    given a project with the pretend_send script imported as the 6th script
    (depends on pretend_mechanics1 and pretend_mechanics2.
    i.e. pretend_send will be executed twice after pretend_mechanics1 and pretend_mechanics2 separately),
    when I run the project,
    should see solution1.txt and solution2.txt sent to a destination folder
    """

    path_1 = os.path.join(pytest.project_root, 'results', 'solution1.txt')
    path_2 = os.path.join(pytest.project_root, 'results', 'solution2.txt')

    assert os.path.isfile(path_1) and os.path.isfile(path_2)
