# SST Elements Installer

The SST core requires at least one [element](http://sst-simulator.org/SSTPages/SSTDeveloperElementSummaryInfo/) (a drivable library) to perform a simulation. As a stand-alone entity, the core fulfills no purpose.

This installer provides users with the capability to manage the elements on their systems. Read [PROPOSAL.md](docs/PROPOSAL.md) for further justification as well as instructions for contribution.

## Table of Contents

- [Installation](#installation)
  - [Production](#production)
  - [Development](#development)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Graphical User Interface](#graphical-user-interface)

## Installation

The installer is packaged in a simple command line interface (CLI) as well as a graphical user interface (GUI). The GUI is built on top of Qt.

### Production

### Development

Export the environment variables required by the program:
```shell
source setup.sh
```

The CLI wrapper of the installer does not require any additional libraries.

To install requirements for the GUI wrapper, a Python virtual environment is recommended.
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```
usage: cli.py [--uninstall <ELEMENT>] [--branch <BRANCH>] [--commit <SHA>]
              [--force] [--list] [--registered [all|<ELEMENT>]]
              [--info <ELEMENT>] [--dep <ELEMENT>] [-h] [-v] [--quiet]
              [<ELEMENT>]

SST Elements Installer

This script provides the functionality required to manage SST elements in a system.

The functionalities include:
    - listing possible elements
    - listing elements registered on system
    - gathering dependency of elements
    - gathering README content of elements
    - cloning elements and its dependencies
    - installing elements and its dependencies to the system
    - uninstalling elements from the system
    - uninstalling dependent elements from the system
    - gathering version of SST Core installed in the system

Installation arguments:
  <ELEMENT>                         Install element along with its dependencies
  --uninstall, -u <ELEMENT>         Uninstall element
  --branch, -b <BRANCH>             Branch of element repository. By default,
                                    the installer will clone the master branch
                                    of the element's repository.
  --commit, -c <SHA>                Commit SHA of element repository. By
                                    default, the installer will clone the
                                    version of the repository at its head.
  --force, -f                       Flag to force installation or removal of
                                    element. If option is applied to
                                    installation, the existing files will be
                                    overwritten by the updated versions. If
                                    option is applied to uninstallation, the
                                    element as well as all its dependent
                                    elements will be removed.

Element information arguments:
  --list, -l                        List all SST elements
  --registered, -r [all|<ELEMENT>]  List elements registered to the system
  --info, -i <ELEMENT>              Display information on element
  --dep, -d <ELEMENT>               Display dependencies of element

Optional arguments:
  -h, --help                        Show this help message and exit
  -v, --version                     Show version number and exit
  --quiet, -q                       Suppress standard outputs
```

### Graphical User Interface
