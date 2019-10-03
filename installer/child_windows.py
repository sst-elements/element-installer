#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, \
    QMainWindow, QPushButton


class ChildWindow(QMainWindow):

    def __init__(self, parent, header, widgets):

        super(ChildWindow, self).__init__(parent)

        self.parent = parent

        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        layout = QVBoxLayout()

        self.header = QLabel()
        self.header.setText(header)

        self.back_btn = QPushButton("Back")

        layout.addWidget(self.header)
        for widget in widgets:
            layout.addWidget(widget)
        layout.addWidget(self.back_btn)

        self.window.setLayout(layout)

        self.back_btn.clicked.connect(self.on_back_clicked)

    def on_back_clicked(self):
        self.hide()
        self.parent.show()
