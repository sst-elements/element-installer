#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sstelements
from templates import ChildWindow


class ElementOptionsWindow(ChildWindow):

    def __init__(self, parent):

        self.about = QtWidgets.QTextEdit()
        self.about.setReadOnly(True)

        if parent.__class__.__name__ == "ElementsWindow":

            self.install_btn = QtWidgets.QPushButton("Install")
            self.uninstall_btn = QtWidgets.QPushButton("Uninstall")

            super(ElementOptionsWindow, self).__init__(
                parent,
                header="Element",
                widgets=[self.about, self.install_btn, self.uninstall_btn]
            )
            self.install_btn.clicked.connect(self.install_element)

        else:

            self.uninstall_btn = QtWidgets.QPushButton("Uninstall")

            super(ElementOptionsWindow, self).__init__(
                parent,
                header="Element",
                widgets=[self.about, self.uninstall_btn]
            )

        self.uninstall_btn.clicked.connect(self.uninstall_element)
        self.element = None

    def set_element(self, element):
        self.element = element
        self.about.setText(sstelements.get_info(self.element))

    def install_element(self):
        sstelements.install(self.element, url="sabbirahm3d")
        self.parent.update()

    def uninstall_element(self):
        sstelements.uninstall(self.element)
        self.parent.update()


class RegisteredElementsWindow(ChildWindow):

    def __init__(self, parent):
        self.list_view = QtWidgets.QListView()

        super(RegisteredElementsWindow, self).__init__(
            parent,
            header="Registered Elements",
            widgets=[self.list_view]
        )
        self.update()
        self.list_view.clicked.connect(self.on_list_view_clicked)
        self.selected_element_window = ElementOptionsWindow(self)

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):
        self.hide()
        self.selected_element_window.set_element(self.reg_elements[index.row()])
        self.selected_element_window.show()

    def update(self):
        self.reg_elements = sstelements.list_registered_elements()
        self.list_view.setModel(QtCore.QStringListModel(self.reg_elements))
        self.list_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


class ElementsWindow(ChildWindow):

    def __init__(self, parent):

        self.list_view = QtWidgets.QListWidget()

        super(ElementsWindow, self).__init__(
            parent,
            header="SST Elements",
            widgets=[self.list_view]
        )

        self.update()
        self.list_view.clicked.connect(self.on_list_view_clicked)
        self.selected_element_window = ElementOptionsWindow(self)

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        self.selected_element_window.set_element(self.all_elements[index.row()])
        self.selected_element_window.show()

    def update(self):
        self.list_view.clear()
        self.all_elements = sstelements._list_all_elements()
        reg_elements = sstelements.list_registered_elements()
        for element in self.all_elements:
            element_item = QtWidgets.QListWidgetItem(element)
            if element in reg_elements:
                element_item.setBackground(QtGui.QColor("#7fc97f"))
            self.list_view.addItem(element_item)
