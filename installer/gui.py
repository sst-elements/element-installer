#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets

from gui import windows

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("SST Elements")
    app.setStyle("Fusion")

    main = windows.MainWindow()
    main.show()

    sys.exit(app.exec_())
