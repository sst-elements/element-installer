#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import sstelements
from .templates import SSTElementWindow, SplashScreen, ElementsListWindow

# suppress all console outputs
sstelements.LOG = False


class ElementOptionsWindow(SSTElementWindow):

    def __init__(self, parent):

        self.parent = parent
        super(ElementOptionsWindow, self).__init__(self.parent)

        self.element = None

        self.install_btn = None
        self.uninstall_btn = None

        self.add_header()

        self.url = QtWidgets.QLabel()
        self.url.setOpenExternalLinks(True)
        self.insert_widget(self.url)

        self.about = QtWidgets.QTextEdit()
        self.about.setReadOnly(True)
        self.insert_widget(self.about)

        self.add_back_btn()
        self.add_exit_btn()
        self.add_hlayout()

    def set_element(self, element):

        self.element = element
        readme, url = sstelements.get_info(self.element)
        self.url.setText(f"<a href='{url}'>{url}</a>")
        self.about.setText(readme)

    def set_registered(self, registered):

        # if element is registered, replace the install button with the uninstall button
        if registered:

            self.set_header(f"{self.element}<font color='#27ae60'> ✓</font>")
            if not self.uninstall_btn:
                self.uninstall_btn = QtWidgets.QPushButton("Uninstall")
                self.uninstall_btn.clicked.connect(
                    lambda: self.element_action(sstelements.uninstall))
                self.insert_widget(self.uninstall_btn, 3)
                self.uninstall_btn.setStyleSheet("background-color: #e74c3c")

            if self.install_btn:
                self.install_btn.deleteLater()
                self.install_btn = None

        # replace the uninstall button with the install button
        else:

            self.set_header(f"{self.element}")
            if not self.install_btn:
                self.install_btn = QtWidgets.QPushButton("Install")
                self.install_btn.clicked.connect(
                    lambda: self.element_action(sstelements.install))
                self.insert_widget(self.install_btn, 3)
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


class RegisteredElementsWindow(ElementsListWindow):

    def __init__(self, parent):

        super(RegisteredElementsWindow, self).__init__(parent, header="Registered Elements")
        self.selected_element_window = ElementOptionsWindow(self)

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        self.selected_element_window.set_element(self.elements[index.row()])
        self.selected_element_window.set_registered(True)
        self.selected_element_window.show()

    def update(self):

        self.list_view.clear()
        self.elements = sstelements.list_registered_elements()
        for element in self.elements:
            element_item = QtWidgets.QListWidgetItem(element)
            element_item.setSelected(False)
            element_item.setIcon(self.default_icon)
            self.list_view.addItem(element_item)


class ElementsWindow(ElementsListWindow):

    def __init__(self, parent):

        super(ElementsWindow, self).__init__(parent, header="SST Elements")
        self.selected_element_window = ElementOptionsWindow(self)

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        element = self.elements[index.row()]
        self.hide()
        self.selected_element_window.set_element(element)
        self.selected_element_window.set_registered(sstelements.is_registered(element))
        self.selected_element_window.show()

    def update(self):

        self.list_view.clear()
        self.elements = list(sstelements.list_all_elements().keys())
        for element in self.elements:
            element_item = QtWidgets.QListWidgetItem(element)
            if sstelements.is_registered(element):
                element_item.setBackground(QtGui.QColor("#2ecc71"))
            element_item.setSelected(False)
            element_item.setIcon(self.default_icon)
            self.list_view.addItem(element_item)


class MainWindow(SSTElementWindow):

    def __init__(self):

        super(MainWindow, self).__init__(None)

        self.intro = QtWidgets.QTextEdit()
        self.intro.setReadOnly(True)
        self.intro.setText(f"""
            <h1>SST Elements</h1>
            <p style='font-size:12px;text-align:center'>{sstelements.get_version()}</p>
        """)
        self.intro.setAlignment(QtCore.Qt.AlignCenter)
        self.intro.setStyleSheet("padding-top: 175")
        self.insert_widget(self.intro)

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
