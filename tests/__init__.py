#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sstelements import sstelements


class TestInstallation(unittest.TestCase):

    element = "hermes"
    parent = "thornhill"
    grandparent = "miranda"

    dependencies = []

    def test_dependency(self):

        self.dependencies.append(self.element)

        self.assertEqual(sstelements.get_dependencies(self.element).pop(), self.parent)
        self.dependencies.append(self.parent)

        self.assertEqual(sstelements.get_dependencies(self.parent).pop(), self.grandparent)
        self.dependencies.append(self.grandparent)

    def test_install_invalid_element(self):
        """Install"""
        self.assertRaises(FileNotFoundError, sstelements.install, element="dummy_element")

    def test_install_element(self):
        """Install"""
        sstelements.install(self.element)
        for element in self.dependencies:
            self.assertTrue(sstelements.is_registered(element))

    def test_uninstall_element(self):
        """Uninstall"""
        sstelements.uninstall(self.parent, clean=True)
        sstelements.uninstall(self.grandparent)
        for element in self.dependencies:
            self.assertFalse(sstelements.is_registered(element))


if __name__ == "__main__":
    # suppress all console outputs
    sstelements.LOG = False
    unittest.main()
