#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import QStringListModel, pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor

import install
from child_windows import ChildWindow


ALL_ELEMENTS = install.list_all_elements()
REG_ELEMENTS = list(install.list_registered_elements())


class ElementOptionsWindow(QMainWindow):

    def __init__(self, parent, registered=True):

        super(ElementOptionsWindow, self).__init__(parent)

        self.parent = parent

        self.push_button = QPushButton("element")
        self.setCentralWidget(self.push_button)
        self.push_button.clicked.connect(self.on_push_back)

    def set_element(self, element):
        print(element)

    def on_push_back(self):
        self.hide()
        self.parent.show()


class RegisteredElementsWindow(ChildWindow):

    def __init__(self, parent):

        self.list_view = QListView()
        self.list_view.setModel(QStringListModel(REG_ELEMENTS))
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        super(RegisteredElementsWindow, self).__init__(
            parent,
            header="Registered Elements",
            widgets=[self.list_view]
        )
        self.list_view.clicked.connect(self.on_list_view_clicked)
        self.selected_element_window = ElementOptionsWindow(self)

    @pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        self.selected_element_window.set_element(REG_ELEMENTS[index.row()])
        self.selected_element_window.show()


class ElementsWindow(ChildWindow):

    def __init__(self, parent):

        self.list_view = QListView()
        self.list_view.setModel(QStringListModel(ALL_ELEMENTS))
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        super(ElementsWindow, self).__init__(
            parent,
            header="SST Elements",
            widgets=[self.list_view]
        )
        self.list_view.clicked.connect(self.on_list_view_clicked)
        self.selected_element_window = ElementOptionsWindow(self)

    @pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        self.selected_element_window.set_element(ALL_ELEMENTS[index.row()])
        self.selected_element_window.show()


class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()

        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        layout = QVBoxLayout()

        self.reg_elems_btn = QPushButton("Registered elements")
        self.install_elems_btn = QPushButton("New elements")

        layout.addWidget(self.reg_elems_btn)
        layout.addWidget(self.install_elems_btn)

        self.window.setLayout(layout)

        self.reg_elems_btn.clicked.connect(self.on_list_elems_clicked)
        self.install_elems_btn.clicked.connect(self.on_install_elems_clicked)

        self.elements_window = ElementsWindow(self)
        self.registered_elements_window = RegisteredElementsWindow(self)

    def set_element(self, element):
        print(element)

    def on_list_elems_clicked(self):
        self.hide()
        self.registered_elements_window.show()

    def on_install_elems_clicked(self):
        self.hide()
        self.elements_window.show()


def main():

    app = QApplication(sys.argv)
    app.setApplicationName("Megasolid Idiom")
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
