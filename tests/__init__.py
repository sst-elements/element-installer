#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from sstelements import sstelements


class TestInstallation(unittest.TestCase):

    element = "hermes"
    parent = "thornhill"
    grandparent = "miranda"

    dependencies = []

    def test_dependency(self):
        """Gather dependency of member elements

        This method verifies the expected dependencies of the elements.
        """
        self.dependencies.append(self.element)

        self.assertEqual(sstelements.get_dependencies(self.element).pop(), self.parent)
        self.dependencies.append(self.parent)

        self.assertEqual(sstelements.get_dependencies(self.parent).pop(), self.grandparent)
        self.dependencies.append(self.grandparent)

    def test_install_invalid_element(self):
        """Install an invalid or unsupported element

        This method raises a FileNotFoundError
        """
        # attempt to install unsupported element "invalid_element"
        self.assertRaises(FileNotFoundError, sstelements.install, element="invalid_element")

    def test_install_element(self):
        """Install an element properly

        This method installs and registers self.element along with its dependencies and verifies
        their registration on the system.
        """
        sstelements.install(self.element)
        for element in self.dependencies:
            self.assertTrue(sstelements.is_registered(element))

    def test_uninstall_element(self):
        """Uninstall an element properly

        This method removes and unregisters self.grandparent along with its dependents and verifies
        their registration on the system.
        """
        sstelements.uninstall(self.parent, clean=True)
        sstelements.uninstall(self.grandparent)
        for element in self.dependencies:
            self.assertFalse(sstelements.is_registered(element))


if __name__ == "__main__":

    # suppress all console outputs
    sstelements.LOG = False
    unittest.main()
