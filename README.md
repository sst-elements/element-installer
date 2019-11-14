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
usage: cli.py [-h] [-v] [--uninstall <ELEMENT>] [--info <ELEMENT>]
              [--dep <ELEMENT>] [--list] [--registered [all|<ELEMENT>]]
              [--branch <BRANCH>] [--head <COMMIT>] [--quiet] [--force]
              [<ELEMENT>]

SST Element Installer

Positional arguments:
  <ELEMENT>                         Install element

Optional arguments:
  -h, --help                        Show this help message and exit
  -v, --version                     Show version number and exit
  --uninstall, -u <ELEMENT>         Uninstall element
  --info, -i <ELEMENT>              Display information on element
  --dep, -d <ELEMENT>               Display dependencies of element
  --list, -l                        List all SST elements
  --registered, -r [all|<ELEMENT>]  List elements registered to the system
  --branch, -b <BRANCH>             Choose branch
  --head, -c <COMMIT>               Choose commit SHA
  --quiet, -q                       Suppress standard outputs
  --force, -f                       Flag to force installation or removal of
                                    element. If option is applied to
                                    installation, the existing files will be
                                    overwritten by the updated versions. If
                                    option is applied to uninstallation, the
                                    element as well as all its dependent
                                    elements will be removed.

```

### Graphical User Interface
