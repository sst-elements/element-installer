# SST Elements
Installer for SST Elements.

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
usage: cli.py [-h] [--install <ELEMENT>] [--uninstall <ELEMENT>] [--quiet]
              [--force] [--list] [--registered] [--url <URL>]
              [--details <ELEMENT>]

SST Element Installer

optional arguments:
  -h, --help                 show this help message and exit
  --install, -i <ELEMENT>    Install element
  --uninstall, -u <ELEMENT>  Uninstall element
  --quiet, -q                Suppress standard outputs
  --force, -f                Force installation
  --list, -l                 List all SST elements
  --registered, -r           List elements registered to the system
  --url, -x <URL>            External URL for element
  --details, -d <ELEMENT>    Display element information

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
