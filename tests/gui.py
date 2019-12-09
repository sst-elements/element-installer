#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore

import os
import sys
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sstelements")
sys.path.append(BASE_DIR)
import sstelements
from gui_test import windows

# suppress all console outputs
sstelements.LOG = False


def test_session(qtbot):

    element = "hermes"
    element_item = 7

    def left_click(btn, **kwargs):
        qtbot.mouseClick(btn, QtCore.Qt.LeftButton, **kwargs)

    window = windows.MainWindow()
    qtbot.addWidget(window)

    left_click(window.install_elems_btn)
    elements_window = window.elements_window
    selected_element_window = elements_window.selected_element_window

    items = []
    elements = elements_window.list_view
    for x in range(elements.count()):
        items.append(elements.item(x).text())

    assert items == list(sstelements.list_all_elements().keys())

    rect = elements.visualItemRect(elements.item(element_item))
    left_click(elements.viewport(), pos=rect.center())
    assert selected_element_window.element == element

    left_click(selected_element_window.install_btn)
    qtbot.wait_until(lambda: selected_element_window.is_registered, timeout=300000)

    left_click(selected_element_window.back_btn)
    left_click(elements_window.back_btn)
    left_click(window.reg_elems_btn)

    registered_elements_window = window.registered_elements_window
    selected_element_window = registered_elements_window.selected_element_window

    items = []
    registered_elements = registered_elements_window.list_view
    for x in range(registered_elements.count()):
        items.append(registered_elements.item(x).text())

    assert items == sstelements.list_registered_elements()

    def uninstall():

        rect = registered_elements.visualItemRect(registered_elements.item(0))
        left_click(registered_elements.viewport(), pos=rect.center())
        left_click(selected_element_window.uninstall_btn)
        qtbot.wait_until(lambda: not selected_element_window.is_registered, timeout=3000)
        left_click(selected_element_window.back_btn)

    for _ in range(registered_elements.count()):
        uninstall()

    assert sstelements.list_registered_elements() == []

    left_click(registered_elements_window.exit_btn)
