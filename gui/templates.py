#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from spinner import QtWaitingSpinner


class RunnableAction(QtCore.QRunnable):
    def __init__(self, window, action, *args):

        QtCore.QRunnable.__init__(self)
        self.window = window
        self.action = action
        self.args = args

    def run(self):

        QtCore.QMetaObject.invokeMethod(
            self.window, "stop",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(int, self.action(*self.args)))


class SplashScreen(QtWidgets.QDialog):

    def __init__(self, parent, element, action, *action_args):

        super(SplashScreen, self).__init__(None)
        self.resize(200, 100)

        self.parent = parent

        self.element = element

        self.action = action
        self.action_args = action_args

        self.setLayout(QtWidgets.QVBoxLayout())

        __header_label = QtWidgets.QLabel()
        __header_label.setText(f"Installing {self.element}...")

        self.spinner = QtWaitingSpinner(self)
        self.layout().addWidget(__header_label)
        self.layout().addWidget(self.spinner)

        self.spinner.start()
        QtCore.QThreadPool.globalInstance().start(
            RunnableAction(self, self.action, self.element, *self.action_args)
        )

    @QtCore.pyqtSlot(int)
    def stop(self):
        self.spinner.stop()
        self.adjustSize()
        self.parent.update()
        self.hide()


class ChildWindow(QtWidgets.QMainWindow):

    def __init__(self, parent, header, widgets):

        super(ChildWindow, self).__init__(parent)
        self.setFixedSize(640, 480)

        self.parent = parent

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

        __window.setLayout(__layout)

        __back_btn.clicked.connect(self.on_back_clicked)
        __exit_btn.clicked.connect(self.on_exit_clicked)

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
