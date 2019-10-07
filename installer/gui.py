#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import QStringListModel, pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor

import install
from child_windows import ChildWindow


class ElementOptionsWindow(ChildWindow):

    def __init__(self, parent, registered=True):

        self.about = QTextEdit()
        self.install_btn = QPushButton("Install")
        self.uninstall_btn = QPushButton("Uninstall")

        super(ElementOptionsWindow, self).__init__(
            parent,
            header="Element",
            widgets=[self.about, self.install_btn, self.uninstall_btn]
        )
        self.install_btn.clicked.connect(self.install_element)
        self.uninstall_btn.clicked.connect(self.uninstall_element)
        self.element = None

    def set_element(self, element):
        self.element = element
        self.about.setText(install.get_info(self.element))

    def install_element(self):
        install.install(self.element, url="sabbirahm3d")
        self.parent.update()

    def uninstall_element(self):
        install.uninstall(self.element)
        self.parent.update()


class RegisteredElementsWindow(ChildWindow):

    def __init__(self, parent):

        self.list_view = QListView()

        super(RegisteredElementsWindow, self).__init__(
            parent,
            header="Registered Elements",
            widgets=[self.list_view]
        )
        self.update()
        self.list_view.clicked.connect(self.on_list_view_clicked)
        self.selected_element_window = ElementOptionsWindow(self)

    @pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        self.selected_element_window.set_element(self.reg_elements[index.row()])
        self.selected_element_window.show()

    def update(self):
        self.reg_elements = install.list_registered_elements()
        self.list_view.setModel(QStringListModel(self.reg_elements))
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)


class ElementsWindow(ChildWindow):

    def __init__(self, parent):

        self.list_view = QListWidget()

        super(ElementsWindow, self).__init__(
            parent,
            header="SST Elements",
            widgets=[self.list_view]
        )

        self.update()
        self.list_view.clicked.connect(self.on_list_view_clicked)
        self.selected_element_window = ElementOptionsWindow(self)

    @pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        self.selected_element_window.set_element(self.all_elements[index.row()])
        self.selected_element_window.show()

    def update(self):
        self.list_view.clear()
        self.all_elements = install._list_all_elements()
        reg_elements = install.list_registered_elements()
        for element in self.all_elements:
            element_item = QListWidgetItem(element)
            if element in reg_elements:
                element_item.setBackground(QColor("#7fc97f"))
            self.list_view.addItem(element_item)


class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
        self.setFixedSize(640, 480)

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

    def on_list_elems_clicked(self):
        self.hide()
        self.registered_elements_window.update()
        self.registered_elements_window.show()

    def on_install_elems_clicked(self):
        self.hide()
        self.elements_window.show()


def main():

    app = QApplication(sys.argv)
    app.setApplicationName("SST Elements")
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
