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
        self._layout = QtWidgets.QVBoxLayout()

        self._header_label = QtWidgets.QLabel()
        self._header_label.setText(f"Installing {self.element}...")

        self.spinner = QtWaitingSpinner(self)

        self.setLayout(self._layout)
        self.layout().addWidget(self._header_label)
        self.layout().addWidget(self.spinner)

        self.spinner.start()
        QtCore.QThreadPool.globalInstance().start(
            RunnableAction(self, self.action, self.element, *self.action_args)
        )

    @QtCore.pyqtSlot(int)
    def stop(self, rdata):

        self.spinner.stop()
        self.adjustSize()
        self.parent.update(rdata)
        self.hide()


class SSTElementWindow(QtWidgets.QMainWindow):

    def __init__(self, parent, widgets):

        super(SSTElementWindow, self).__init__(parent)
        self.setFixedSize(640, 480)

        self.parent = parent

        self._window = QtWidgets.QWidget(self)
        self.setCentralWidget(self._window)
        self._layout = QtWidgets.QVBoxLayout()

        self._header_label = QtWidgets.QLabel()
        # self.set_header(header)

        self._layout.addWidget(self._header_label)
        for widget in widgets:
            self._layout.addWidget(widget)

        self._back_btn = QtWidgets.QPushButton("Back")
        self._exit_btn = QtWidgets.QPushButton("Exit")

        self._hlayout = QtWidgets.QHBoxLayout()
        self._hlayout.addWidget(self._back_btn)
        self._hlayout.addWidget(self._exit_btn)
        self._layout.addLayout(self._hlayout)

        self._window.setLayout(self._layout)
        self.setStyleSheet("background-color: #ecf0f1")

        self._back_btn.clicked.connect(self.on_back_clicked)
        self._exit_btn.clicked.connect(self.on_exit_clicked)

    def set_header(self, header):

        self._header_label.setText(header)

    def on_back_clicked(self):

        self.hide()
        self.parent.update()
        self.parent.show()

    def on_exit_clicked(self):

        self.close()
