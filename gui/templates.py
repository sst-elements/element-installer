#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from spinner import QtWaitingSpinner


class RequestRunnable(QtCore.QRunnable):
    def __init__(self, window, action, *args):

        QtCore.QRunnable.__init__(self)
        self.window = window
        self.action = action
        self.args = args

    def run(self):

        QtCore.QMetaObject.invokeMethod(
            self.window, "set_data",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(int, self.action(*self.args)))


class ChildWindow(QtWidgets.QMainWindow):

    def __init__(self, parent, header, widgets):

        super(ChildWindow, self).__init__(parent)
        self.setFixedSize(640, 480)

        self.parent = parent
        self.spinner = QtWaitingSpinner(self)

        __window = QtWidgets.QWidget(self)
        self.setCentralWidget(__window)
        __layout = QtWidgets.QVBoxLayout()

        __header_label = QtWidgets.QLabel()
        __header_label.setText(f"<h1>{header}</h1>")

        __layout.addWidget(__header_label)
        for widget in widgets:
            __layout.addWidget(widget)

        __back_btn = QtWidgets.QPushButton("Back")
        __exit_btn = QtWidgets.QPushButton("Exit")

        __hlayout = QtWidgets.QHBoxLayout()
        __hlayout.addWidget(__back_btn)
        __hlayout.addWidget(__exit_btn)
        __layout.addLayout(__hlayout)
        __layout.addWidget(self.spinner)

        __window.setLayout(__layout)

        __back_btn.clicked.connect(self.on_back_clicked)
        __exit_btn.clicked.connect(self.on_exit_clicked)

        self.runnable = RequestRunnable

    @QtCore.pyqtSlot(int)
    def set_data(self):

        self.spinner.stop()
        self.adjustSize()
        self.parent.update()

    def on_back_clicked(self):

        self.hide()
        self.parent.show()

    def on_exit_clicked(self):

        self.close()


class ColorPalette(QtGui.QPalette):

    def __init__(self):

        super(ColorPalette, self).__init__()

        self.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        self.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
        self.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        self.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        self.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 255))
        self.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
        self.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
        self.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        self.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
        self.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
        self.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        self.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        self.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
