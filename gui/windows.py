#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sstelements
from templates import ChildWindow, SplashScreen


class ElementOptionsWindow(ChildWindow):

    def __init__(self, parent):

        self.about = QtWidgets.QTextEdit()
        self.about.setReadOnly(True)
        self.parent = parent

        if parent.__class__.__name__ == "ElementsWindow":

            self.install_btn = QtWidgets.QPushButton("Install")
            self.uninstall_btn = QtWidgets.QPushButton("Uninstall")

            super(ElementOptionsWindow, self).__init__(
                parent,
                header="Element",
                widgets=[self.about, self.install_btn, self.uninstall_btn]
            )
            self.install_btn.clicked.connect(
                lambda: self.element_action(sstelements.install, "sabbirahm3d"))

        else:

            self.uninstall_btn = QtWidgets.QPushButton("Uninstall")

            super(ElementOptionsWindow, self).__init__(
                parent,
                header="Element",
                widgets=[self.about, self.uninstall_btn]
            )

        self.uninstall_btn.clicked.connect(lambda: self.element_action(sstelements.uninstall))
        self.element = None

    def set_registered(self, registered):

        self.registered = registered
        self._header_label.setText(f"<h1>{self.element}{(' ✓' if self.registered else '')}</h1>")

    def set_element(self, element):

        self.element = element
        self.about.setText(sstelements.get_info(self.element))

    def element_action(self, *action_args):

        splash = SplashScreen(self, self.element, *action_args)
        splash.setWindowModality(QtCore.Qt.ApplicationModal)
        splash.show()

    def update(self, rdata):

        if rdata == 1:
            self.set_registered(False)

        elif rdata == 2:
            self.set_registered(True)
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
        self.selected_element_window.set_registered(True)
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
        element = self.all_elements[index.row()]
        self.selected_element_window.set_element(element)
        self.selected_element_window.set_registered(sstelements.is_registered(element))
        self.selected_element_window.show()

    def update(self):

        self.list_view.clear()
        self.all_elements = sstelements._list_all_elements()
        for element in self.all_elements:
            element_item = QtWidgets.QListWidgetItem(element)
            if sstelements.is_registered(element):
                element_item.setBackground(QtGui.QColor("#7fc97f"))
            element_item.setSelected(False)
            self.list_view.addItem(element_item)


class MainWindow(ChildWindow):

    def __init__(self):

        self.reg_elems_btn = QtWidgets.QPushButton("Registered elements")
        self.install_elems_btn = QtWidgets.QPushButton("New elements")

        super(MainWindow, self).__init__(
            None,
            header="SST Elements",
            widgets=[self.reg_elems_btn, self.install_elems_btn]
        )

        self.reg_elems_btn.clicked.connect(self.on_list_elems_clicked)
        self.install_elems_btn.clicked.connect(self.on_install_elems_clicked)

        self.elements_window = ElementsWindow(self)
        self.registered_elements_window = RegisteredElementsWindow(self)

    def on_list_elems_clicked(self):

        self.hide()
        self.registered_elements_window.update()
        self.registered_elements_window.show()

    def on_install_elems_clicked(self):

        self.hide()
        self.elements_window.update()
        self.elements_window.show()
