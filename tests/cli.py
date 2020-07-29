#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import sys

import pytest

BASE_DIR = Path(__file__).absolute().parent.parent / "installer"
sys.path.append(str(BASE_DIR))
import installer

# suppress all console outputs
installer.LOG = False

ELEMENT = "hermes"
PARENT = "thornhill"
GRANDPARENT = "miranda"

DEPENDENCIES = []


def test_dependency():
    """Gather dependency of member elements

    This method verifies the expected dependencies of the elements.
    """
    DEPENDENCIES.append(ELEMENT)

    assert installer.get_dependencies(ELEMENT).pop() == PARENT
    DEPENDENCIES.append(PARENT)

    assert installer.get_dependencies(PARENT).pop() == GRANDPARENT
    DEPENDENCIES.append(GRANDPARENT)


def test_install_invalid_element():
    """Install an invalid or unsupported element

    This method raises a FileNotFoundError
    """
    # attempt to install unsupported element "invalid_element"
    with pytest.raises(FileNotFoundError):
        installer.install(element="invalid_element")


def test_install_element():
    """Install an element properly

    This method installs and registers element along with its dependencies and verifies
    their registration on the system.
    """
    installer.install(ELEMENT)
    for element in DEPENDENCIES:
        assert installer.is_registered(element)


def test_uninstall_element():
    """Uninstall an element properly

    This method removes and unregisters grandparent along with its dependents and verifies
    their registration on the system.
    """
    installer.uninstall(PARENT, clean=True)
    installer.uninstall(GRANDPARENT)
    for element in DEPENDENCIES:
        assert not installer.is_registered(element)
