Examples
========

To run the examples.

1. Install the Python dependencies using pip and virtual environment (recommended).

   1.1. Create a virtual environment

      .. code-block:: bash

         python3 -m venv venv/

   1.2. Activate the virtual environment

      - Linux

         .. code-block:: bash

            source venv/bin/activate

      - Windows

         .. code-block:: bash

            venv\Scripts\activate

   1.3. Update pip

      .. code-block:: bash

         pip install --upgrade pip

   1.4. Install the dependencies

      .. code-block:: bash

         pip install -r requirements.txt

2. Change directory to examples folder

   .. code-block:: bash

      cd workflow/examples/

3. Run this example script - This will setup the pipeline including the scripts that need to be run.
4. To see a list of the processes, open a new Python console/terminal, and run

   .. code-block:: python

      import workflow_manager as wm
      P = wm.Project('test_project')
      P.list_processes()

5. To look at a given processes log, type

   .. code-block:: python

       P.process(process_id).log()
       where "process_id" is the process id from the P.list_process() function.
