#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib.request

from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sstelements
from templates import SSTElementWindow, SplashScreen, get_default_icon


class ElementOptionsWindow(SSTElementWindow):

    def __init__(self, parent, element):

        self.parent = parent
        super(ElementOptionsWindow, self).__init__(self.parent)

        self.element = element

        self.install_btn = None
        self.uninstall_btn = None

        self.add_header()

        self.about = QtWidgets.QTextEdit()
        self.about.setReadOnly(True)
        self.about.setText(sstelements.get_info(self.element))
        self.insert_widget(self.about)

        self.add_back_btn()
        self.add_exit_btn()
        self.add_hlayout()

    def set_registered(self, registered):

        self.set_header(f"{self.element}{' ✓' if registered else ''}")

        # if element is registered, replace the install button with the uninstall button
        if registered:

            if not self.uninstall_btn:
                self.uninstall_btn = QtWidgets.QPushButton("Uninstall")
                self.uninstall_btn.clicked.connect(
                    lambda: self.element_action(sstelements.uninstall))
                self.insert_widget(self.uninstall_btn, 2)
                self.uninstall_btn.setStyleSheet("background-color: #e74c3c")

            if self.install_btn:
                self.install_btn.deleteLater()
                self.install_btn = None

        # replace the uninstall button with the install button
        else:

            if not self.install_btn:
                self.install_btn = QtWidgets.QPushButton("Install")
                self.install_btn.clicked.connect(
                    lambda: self.element_action(sstelements.install))
                self.insert_widget(self.install_btn, 2)
                self.install_btn.setStyleSheet("background-color: #27ae60")

            if self.uninstall_btn:
                self.uninstall_btn.deleteLater()
                self.uninstall_btn = None

    def element_action(self, *action_args):

        splash = SplashScreen(self, self.element, *action_args)
        splash.setWindowModality(QtCore.Qt.ApplicationModal)
        splash.show()

    def update(self, rdata):

        self.set_registered(not rdata)
        self.parent.update()


class RegisteredElementsWindow(SSTElementWindow):

    def __init__(self, parent):

        super(RegisteredElementsWindow, self).__init__(parent)

        self.add_header()
        self.set_header("Registered Elements")

        self.list_view = QtWidgets.QListWidget()
        self.list_view.setViewMode(QtWidgets.QListView.IconMode)
        self.list_view.setIconSize(QtCore.QSize(500, 500))
        self.insert_widget(self.list_view)

        self.add_back_btn()
        self.add_exit_btn()
        self.add_hlayout()

        self.reg_elements = None
        self.list_view.clicked.connect(self.on_list_view_clicked)

        self.default_icon = get_default_icon()

        self.update()

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        selected_element_window = ElementOptionsWindow(self, self.reg_elements[index.row()])
        selected_element_window.set_registered(True)
        selected_element_window.show()

    def update(self):

        self.list_view.clear()
        self.reg_elements = sstelements.list_registered_elements()
        for element in self.reg_elements:
            element_item = QtWidgets.QListWidgetItem(element)
            element_item.setSelected(False)
            element_item.setIcon(self.default_icon)
            self.list_view.addItem(element_item)


class ElementsWindow(SSTElementWindow):

    def __init__(self, parent):

        super(ElementsWindow, self).__init__(parent)

        self.add_header()
        self.set_header("SST Elements")

        self.list_view = QtWidgets.QListWidget()
        self.list_view.setViewMode(QtWidgets.QListView.IconMode)
        self.list_view.setIconSize(QtCore.QSize(500, 500))
        self.insert_widget(self.list_view)

        self.add_back_btn()
        self.add_exit_btn()
        self.add_hlayout()

        self.all_elements = None
        self.list_view.clicked.connect(self.on_list_view_clicked)

        self.default_icon = get_default_icon()

        self.update()

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        element = self.all_elements[index.row()]
        self.hide()
        selected_element_window = ElementOptionsWindow(self, element)
        selected_element_window.set_registered(sstelements.is_registered(element))
        selected_element_window.show()

    def update(self):

        self.list_view.clear()
        self.all_elements = sstelements._list_all_elements()
        for element in self.all_elements:
            element_item = QtWidgets.QListWidgetItem(element)
            if sstelements.is_registered(element):
                element_item.setBackground(QtGui.QColor("#2ecc71"))
            element_item.setSelected(False)
            element_item.setIcon(self.default_icon)
            self.list_view.addItem(element_item)


class MainWindow(SSTElementWindow):

    def __init__(self):

        super(MainWindow, self).__init__(None)

        img_url = "http://sst-simulator.org/img/sst-logo-small.png"
        img_data = urllib.request.urlopen(urllib.request.Request(img_url)).read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(img_data)
        pixmap_label = QtWidgets.QLabel()
        pixmap_label.setPixmap(pixmap)
        pixmap_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        pixmap_label.resize(pixmap.height(), pixmap.width())
        self.insert_widget(pixmap_label)

        reg_elems_btn = QtWidgets.QPushButton("Registered elements")
        self.insert_widget(reg_elems_btn)

        install_elems_btn = QtWidgets.QPushButton("New elements")
        self.insert_widget(install_elems_btn)

        self.add_exit_btn()
        self.add_hlayout()

        reg_elems_btn.clicked.connect(self.on_list_elems_clicked)
        install_elems_btn.clicked.connect(self.on_install_elems_clicked)

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
