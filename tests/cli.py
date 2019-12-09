#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pytest

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sstelements")
sys.path.append(BASE_DIR)
import sstelements

# suppress all console outputs
sstelements.LOG = False

ELEMENT = "hermes"
PARENT = "thornhill"
GRANDPARENT = "miranda"

DEPENDENCIES = []


def test_dependency():
    """Gather dependency of member elements

    This method verifies the expected dependencies of the elements.
    """
    DEPENDENCIES.append(ELEMENT)

    assert sstelements.get_dependencies(ELEMENT).pop() == PARENT
    DEPENDENCIES.append(PARENT)

    assert sstelements.get_dependencies(PARENT).pop() == GRANDPARENT
    DEPENDENCIES.append(GRANDPARENT)


def test_install_invalid_element():
    """Install an invalid or unsupported element

    This method raises a FileNotFoundError
    """
    # attempt to install unsupported element "invalid_element"
    with pytest.raises(FileNotFoundError):
        sstelements.install(element="invalid_element")


def test_install_element():
    """Install an element properly

    This method installs and registers element along with its dependencies and verifies
    their registration on the system.
    """
    sstelements.install(ELEMENT)
    for element in DEPENDENCIES:
        assert sstelements.is_registered(element)


def test_uninstall_element():
    """Uninstall an element properly

    This method removes and unregisters grandparent along with its dependents and verifies
    their registration on the system.
    """
    sstelements.uninstall(PARENT, clean=True)
    sstelements.uninstall(GRANDPARENT)
    for element in DEPENDENCIES:
        assert not sstelements.is_registered(element)
