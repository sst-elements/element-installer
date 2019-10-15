# SST Elements Installer

The SST core requires at least one [element](http://sst-simulator.org/SSTPages/SSTDeveloperElementSummaryInfo/) (a drivable library) to perform a simulation. As a stand-alone entity, the core fulfills no purpose.

This installer provides users with the capability to manage the elements on their systems. Read [PROPOSAL.md](PROPOSAL.md) for further justification as well as details for contribution.

## Table of Contents

- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Graphical User Interface](#graphical-user-interface)
- [Installation](#installation)
  - [Production](#production)
  - [Development](#development)
    - [Cython](#cython)

## Usage

The installer is packaged in a simple command line interface (CLI) as well as a graphical user interface (GUI). The GUI is built on top of Qt.

### Command Line Interface

```
usage: cli.py [-h] [--install <ELEMENT>] [--uninstall <ELEMENT>]
              [--details <ELEMENT>] [--list] [--registered] [--quiet] [--force]

SST Element Installer

optional arguments:
  -h, --help                 show this help message and exit
  --install, -i <ELEMENT>    Install element
  --uninstall, -u <ELEMENT>  Uninstall element
  --details, -d <ELEMENT>    Display element information
  --list, -l                 List all SST elements
  --registered, -r           List elements registered to the system
  --quiet, -q                Suppress standard outputs
  --force, -f                Force installation

```

### Graphical User Interface


## Installation

### Production

### Development

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
source setup.sh
```

#### Cython
