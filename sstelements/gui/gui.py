#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets

from windows import MainWindow

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("SST Elements")
    app.setStyle("Fusion")

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
