#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
    QMainWindow, QPushButton


class ChildWindow(QMainWindow):

    def __init__(self, parent, header, widgets):

        super(ChildWindow, self).__init__(parent)
        self.setFixedSize(640, 480)

        self.parent = parent

        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        layout = QVBoxLayout()

        self.header = QLabel()
        self.header.setText(f"<h1>{header}</h1>")

        layout.addWidget(self.header)
        for widget in widgets:
            layout.addWidget(widget)

        self.back_btn = QPushButton("Back")
        self.exit_btn = QPushButton("Exit")

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.back_btn)
        h_layout.addWidget(self.exit_btn)
        layout.addLayout(h_layout)

        self.window.setLayout(layout)

        self.back_btn.clicked.connect(self.on_back_clicked)
        self.exit_btn.clicked.connect(self.on_exit_clicked)

    def on_back_clicked(self):

        self.hide()
        self.parent.show()

    def on_exit_clicked(self):

        self.close()
