Testing
=======

``Pytest`` is the test framework adopted in this project.
All the tests can be found in the ``tests/`` folder.

To enable Pytest in Pycharm, please see `Enable Pytest in Pycharm <https://www.jetbrains.com/help/pycharm/pytest.html>`_.

For developers, if you want to write more tests, please follow the `Pytest naming convention <https://docs.pytest.org/en/reorganize-docs/new-docs/user/naming_conventions.html>`_

Unit tests
----------

.. automodule:: tests

Functional testing
^^^^^^^^^^^^^^^^^^

.. automethod:: test_functionalities.test_create_project

.. automethod:: test_functionalities.test_create_existing_project

Integration testing
^^^^^^^^^^^^^^^^^^^

Below are the tests for testing the example workflow and its components

.. automethod:: test_example_workflow.test_pretend_import
.. automethod:: test_example_workflow.test_pretend_segment
.. automethod:: test_example_workflow.test_pretend_fit
.. automethod:: test_example_workflow.test_pretend_mechanics
.. automethod:: test_example_workflow.test_pretend_send





