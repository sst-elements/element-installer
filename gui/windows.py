#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sstelements
from templates import SSTElementWindow, SplashScreen


class ElementOptionsWindow(SSTElementWindow):

    def __init__(self, parent, element):

        self.parent = parent
        self.element = element
        self.about = QtWidgets.QTextEdit()
        self.about.setReadOnly(True)
        self.about.setText(sstelements.get_info(self.element))

        self.install_btn = None
        self.uninstall_btn = None

        super(ElementOptionsWindow, self).__init__(
            self.parent,
            widgets=[self.about]
        )

    def set_registered(self, registered):

        self.set_header(f"<h1>{self.element}{(' ✓' if registered else '')}</h1>")

        if registered:

            if not self.uninstall_btn:
                self.uninstall_btn = QtWidgets.QPushButton("Uninstall")
                self.uninstall_btn.clicked.connect(
                    lambda: self.element_action(sstelements.uninstall))
                self._layout.insertWidget(2, self.uninstall_btn)

            if self.install_btn:
                self.install_btn.deleteLater()
                self.install_btn = None

        else:

            if not self.install_btn:
                self.install_btn = QtWidgets.QPushButton("Install")
                self.install_btn.clicked.connect(
                    lambda: self.element_action(sstelements.install, "sabbirahm3d"))
                self._layout.insertWidget(2, self.install_btn)

            if self.uninstall_btn:
                self.uninstall_btn.deleteLater()
                self.uninstall_btn = None

    def element_action(self, *action_args):

        splash = SplashScreen(self, self.element, *action_args)
        splash.setWindowModality(QtCore.Qt.ApplicationModal)
        splash.show()

    def update(self, rdata):

        # just uninstalled
        if rdata:
            self.set_registered(False)

        # just installed
        else:
            self.set_registered(True)

        self.parent.update()


class RegisteredElementsWindow(SSTElementWindow):

    def __init__(self, parent):

        self.list_view = QtWidgets.QListView()

        super(RegisteredElementsWindow, self).__init__(
            parent,
            widgets=[self.list_view]
        )
        self.set_header("<h1>Registered Elements</h1>")

        self.update()
        self.list_view.clicked.connect(self.on_list_view_clicked)

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        self.selected_element_window = ElementOptionsWindow(self, self.reg_elements[index.row()])
        self.selected_element_window.set_registered(True)
        self.selected_element_window.show()

    def update(self):

        self.reg_elements = sstelements.list_registered_elements()
        self.list_view.setModel(QtCore.QStringListModel(self.reg_elements))
        self.list_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


class ElementsWindow(SSTElementWindow):

    def __init__(self, parent):

        self.list_view = QtWidgets.QListWidget()

        super(ElementsWindow, self).__init__(
            parent,
            widgets=[self.list_view]
        )
        self.set_header("<h1>SST Elements</h1>")

        self.update()
        self.list_view.clicked.connect(self.on_list_view_clicked)

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        element = self.all_elements[index.row()]
        self.hide()
        self.selected_element_window = ElementOptionsWindow(self, element)
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


class MainWindow(SSTElementWindow):

    def __init__(self):

        self.reg_elems_btn = QtWidgets.QPushButton("Registered elements")
        self.install_elems_btn = QtWidgets.QPushButton("New elements")

        super(MainWindow, self).__init__(
            None,
            widgets=[self.reg_elems_btn, self.install_elems_btn]
        )
        self.set_header("<p style=\"text-align: center\"><h1>SST Elements</h1>")

        self.reg_elems_btn.clicked.connect(self.on_list_elems_clicked)
        self.install_elems_btn.clicked.connect(self.on_install_elems_clicked)

        self.elements_window = ElementsWindow(self)
        self.registered_elements_window = RegisteredElementsWindow(self)
        if self._back_btn:
            self._back_btn.deleteLater()
            self._back_btn = None

    def on_list_elems_clicked(self):

        self.hide()
        self.registered_elements_window.update()
        self.registered_elements_window.show()

    def on_install_elems_clicked(self):

        self.hide()
        self.elements_window.update()
        self.elements_window.show()
