
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


@pytest.fixture
def delete_project_before():
    delete_project_from_db(pytest.project_name, pytest.conn)
    delete_project_root(pytest.project_root)


@pytest.fixture
def delete_project_after():
    yield
    delete_project_from_db(pytest.project_name, pytest.conn)
    delete_project_root(pytest.project_root)


def test_create_project(delete_project_before, delete_project_after):
    P = wm.create_project(pytest.project_name, root_dir=pytest.project_root)

    assert pytest.project_name in pytest.conn.list_database_names()
    assert P.root_dir == os.path.abspath(pytest.project_root)


def test_create_existing_project(delete_project_before, delete_project_after):
    # given a existing project name,
    # When I try to create an existing project,
    # should get exception when the project already exists

    wm.create_project(pytest.project_name, root_dir=pytest.project_root)

    with pytest.raises(Exception):
        wm.create_project(pytest.project_name, root_dir=pytest.project_root)

