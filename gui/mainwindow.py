#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from windows import ElementsWindow, RegisteredElementsWindow


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(640, 480)

        self.window = QtWidgets.QWidget(self)
        self.setCentralWidget(self.window)
        layout = QtWidgets.QVBoxLayout()

        self.reg_elems_btn = QtWidgets.QPushButton("Registered elements")
        self.install_elems_btn = QtWidgets.QPushButton("New elements")

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
