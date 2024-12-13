# mergetb

This package contains a client interface to the MergeTB API.

## Structure

This package implements classes that reflect the core objects defined by the
[MergeTB API](https://mergetb.gitlab.io/api), including:
- Identity
- User
- Project
- Organization
- Experiment
- Realization
- Materialization
- XDC

Each of these classes implements a GRPC client interface that allows object data to be pushed to /
pulled from a MergeTB portal.

## Example

The following example shows how a user can log into a MergeTB portal and list the projects they
belong to:

```python
import mergetb.mergetb as mergetb
from mergetb.identity import Identity
from mergetb.grpc_client import MergeGRPCError

# login
username = 'xxx' # replace with your MergeTB account username
password = 'xxx' # replace with your MergeTB account password

try:
    identity = Identity(username, password)
    identity.login()

    # get projects
    projects = mergetb.get_projects().projects
    print("Username %s has the following projects:" % username)
    for project in projects:
        summary="""Project: %s
    Description:  %s
    Members:      %s
    Experiments:  %s
    Access Mode:  %d
    GID:          %d
    Organization: %s
    Category:     %s
    Subcategory:  %s""" % (
            project.name,
            project.description,
            project.members,
            project.experiments,
            project.access_mode,
            project.gid,
            project.organization,
            project.category,
            project.subcategory,
        )
        print(summary)
except MergeGRPCError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## API objects

Note that this package is a wrapper around the [mergetbapi](https://pypi.org/project/mergetbapi/), a
separate Python package which provides Python language bindings for the data structures defined in
the [Merge API specification](https://mergetb.gitlab.io/api). This library should be understood as a
wrapper around the `mergetbapi` package that provides a more convenient interface for users to work
with.

## Tests

There are tests defined in the [tests](./tests) directory that show further
examples of how this package can be used to interact with a MergeTB portal:
- test_identity.py
- test_user.py
- test_workflow.py

To run a test, do the following. __NOTE: tests must be run from the package's root directory__:
```bash
python3 -m tests.test_<testname>.py
```

Pass the `-h` option to see what command line options the test accepts; e.g., for the
`test_identity` test:
```bash
python3 -m tests.test_identity -h
usage: test_identity.py [-h] [-u USERNAME] [-p PASSWORD] [-S SERVER] [-P PORT] [-X]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username for your MergeTB account
  -p PASSWORD, --password PASSWORD
                        Password for your MergeTB account
  -S SERVER, --server SERVER
                        MergeTB portal GRPC address
  -P PORT, --port PORT  MergeTB portal GRPC port
  -X, --disable-tls     Disable TLS when communication with the MergeTB portal
```
