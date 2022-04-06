Future
======

How do you manage data and the processing of data in a structured yet
flexible way? Currently, the typical way is to store data on user
filesystems in ad hoc directory structures and process them manually.
The problem is that data can get lost, and if it is not lost, how the
data was generated or processed is lost.

So how do we improve on this? There are two approaches: design the
ultimate system, then build and use it; or design the minimal system,
build and use it, then evolve to the ultimate system. The Workflow Manager package(WM) is the latter,
hence there are many missing features: authentication, access control,
remote access, required and structured data paradigms (e.g., rdf, ontologies).
We know how to build these but they take time, hence these will evolve
into the system as they are needed. The great thing about this approach
is that it’s based on user experience, as opposed to imagined ways of use.
The disadvantage of this approach is that it will change regularly,
however, data can be migrated, so previous work is not lost.

In summary, WM is an experimental system that will hopefully evolve
into a useful and user friendly system.

The following are ideas that will be useful for future developments.
Some questions to ask when adding a feature:

Does it solve a problem?
Does it add more or reduce work for the user?


Pipelines vs’ Broadcast/Listeners
---------------------------------

The current method for processing a pipeline is to create a job with a
list of processes that get queued. Maybe a better and more flexible method
is to create a broadcast/listener system. In this case, you would register
your scripts with a unique label, which has to be agreed amongst users.  
A script will also have a list of scripts it listens to.

For example, the ‘fit breast mesh’ script might listen for when ‘segment
breast MRI’ script is run and when it does, it would execute itself based
on the data produced by the segment script. Another example, is for
creating a PCA mesh of the breast, the ‘generate breast PCA mesh’
scripts might listen for executions by the ‘fit breast mesh’ and if
the fit was successful and its error was below a threshold, it would
add the breast mesh to the PCA mesh, and even version the PCA mesh.
This broadcast/listen system can also be used to notify users via
email or a website of changes.

The advantage of this system is that it does not rely on ensuring when
someone runs a script, they know what other scripts to run. Those
decisions are made by the scripts listening to them. Also scripts
can be informed of updates to upsteam scripts or re-processing
of data, and its up to the downstream script to decide what
to do.
DONE


Version Control of Scripts
--------------------------

It should be possible to register a repository with a script where a
project can be commanded to pull the latest version from the repository.
In this case WM can automatically record the version of scripts data
was processed or generated with.

Furthermore, it might be possible to modify a script in a version control
system and ask a project to test the version against the data and report
the changes or errors. This allows user to check the effect of changes
before committing them to widespread use.

Update:
The current version of WM has the structure to implement this
functionality. One can add the source of the script which has a path
and update mode. The path defines where to find the script, for
example, file, http or version controlled repository path. The
update mode tells the project how to update the script from the
path. Copy functionality is there, where one can run
“script.update_from_source()” and the script will be copied.
There is no support for http or repositories and tracking of versions yet.

Another idea is to implement a “script.test_from_source()” function that
can test the source scripts in a sandbox type environment to ensure it
runs correctly. This could be commanded to run on one pipeline, many pipelines
(manually or randomly defined) or all pipelines that use the script in the
existing project and report differences.


Storing Ancestors and Descendants
---------------------------------
This stores the relationships between workspaces and data stored in
workspaces. This allows the ability to track how data is created and
what data might be affected downstream is data is changed.

Currently, this kind of happens via job creation and scripts. It needs
to be improved however, this may be easier to improve if broadcast/listeners
were used instead of fixed pipelines.

Update:
This is currently in place but not formalised. The processes and workspaces
know about their parents and children but no functions to determine and
report ancestors or descendents. It may be worth saving this with each
process or workspace, including the root ancestor.


Checks and Locking
------------------
Sometimes it is useful to manually check processed data is correct and if
it is, lock the data such that it cannot be changed. This needs to be
implemented.


Logging
-------
A better logging system needs to be implemented that tracks the version
history of data. This is so that when someone uses data outside of the
project, the origin of the data and its processes can be accounted for.


Notifications
-------------
Web-based or email notifications of certain actions or results.


Collections
-----------

Collections is a way to link workspaces together is a tree or graph form.
 Workspaces are a flat structure, the only link between them is through
the flow of data, there is no link in terms of similar data, i.e., data
from the same study, or scans from the same patient. This will need to
be nutted out but I suspect workspaces could be added to collections
manually or automatically via scripts.

It might be possible to store the collections details in such a way that
data is a collection can be viewed in different graph hierarchy, for
example, present by gender, then scan modality, then patient, then
timestamp, or alternatively, present by patient, then scan modality.
