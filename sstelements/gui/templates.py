#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request

from PyQt5 import QtCore, QtGui, QtWidgets

from .spinner import QtWaitingSpinner
import sstelements


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
            QtCore.Q_ARG(int, self.action(*self.args))
        )


class SplashScreen(QtWidgets.QDialog):

    def __init__(self, parent, element, action, *action_args):

        super(SplashScreen, self).__init__(None)
        self.resize(200, 100)

        self.parent = parent
        self.element = element
        self.action = action
        self.action_args = action_args
        self.__layout = QtWidgets.QVBoxLayout()

        self.setLayout(self.__layout)

        header_label = QtWidgets.QLabel()
        header_label.setText(f"Installing {self.element}...")
        header_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.layout().addWidget(header_label)

        self.__spinner = QtWaitingSpinner(self)
        self.layout().addWidget(self.__spinner)

        self.__spinner.start()
        QtCore.QThreadPool.globalInstance().start(
            RunnableAction(self, self.action, self.element, *self.action_args)
        )

    @QtCore.pyqtSlot(int)
    def stop(self, rdata):

        QtWidgets.QMessageBox.information(
            self, "Success",
            f"{'Uninstalled ' + self.element if rdata else sstelements.INSTALLED_ELEMS}"
        )
        self.__spinner.stop()
        self.adjustSize()
        self.parent.update(rdata)
        self.hide()


class SSTElementWindow(QtWidgets.QMainWindow):

    def __init__(self, parent):

        self.parent = parent
        super(SSTElementWindow, self).__init__(self.parent)

        self.setFixedSize(640, 480)

        self.__header_label = None
        self.__layout = QtWidgets.QVBoxLayout()
        self.__hlayout = QtWidgets.QHBoxLayout()

        window = QtWidgets.QWidget(self)
        window.setLayout(self.__layout)
        self.setCentralWidget(window)
        self.setStyleSheet("background-color: #ecf0f1")

    def insert_widget(self, widget, index=0):

        if not index:
            self.__layout.addWidget(widget)
        else:
            self.__layout.insertWidget(index, widget)

    def add_header(self):

        self.__header_label = QtWidgets.QLabel()
        self.__layout.addWidget(self.__header_label)

    def add_back_btn(self):

        back_btn = QtWidgets.QPushButton("← Back")
        self.__hlayout.addWidget(back_btn)
        back_btn.clicked.connect(self.__on_back_clicked)

    def add_exit_btn(self):

        exit_btn = QtWidgets.QPushButton("❌ Exit")
        exit_btn.setStyleSheet("background-color: #34495e; color: #fff")
        self.__hlayout.addWidget(exit_btn)
        exit_btn.clicked.connect(self.__on_exit_clicked)

    def add_hlayout(self):

        self.__hlayout.setAlignment(QtCore.Qt.AlignRight)
        self.__layout.addLayout(self.__hlayout)

    def set_header(self, header):

        self.__header_label.setText(f"<h1>{header}</h1>")

    def __on_back_clicked(self):

        self.hide()
        self.parent.update()
        self.parent.show()

    def __on_exit_clicked(self):

        self.close()


class ElementsListWindow(SSTElementWindow):

    def __init__(self, parent, header):

        super(ElementsListWindow, self).__init__(parent)

        self.add_header()
        self.set_header(header)

        self.list_view = QtWidgets.QListWidget()
        self.list_view.setViewMode(QtWidgets.QListView.IconMode)
        self.list_view.setIconSize(QtCore.QSize(500, 500))
        self.insert_widget(self.list_view)

        self.add_back_btn()
        self.add_exit_btn()
        self.add_hlayout()

        self.elements = None
        self.list_view.clicked.connect(self.on_list_view_clicked)

        self.default_icon = get_default_icon()

        self.update()


def get_default_icon():

    img_url = "http://sst-simulator.org/img/sst-logo-small.png"
    img_data = urllib.request.urlopen(urllib.request.Request(img_url)).read()
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(img_data)
    icon = QtGui.QIcon()
    icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)

    return icon
