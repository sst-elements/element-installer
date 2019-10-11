#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtWidgets

from windows import MainWindow

if __name__ == "__main__":

    with open(os.devnull, "w") as devnull:
        # suppress all console outputs
        sys.stdout = devnull

        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("SST Elements")
        app.setStyle("Fusion")

        main = MainWindow()
        main.show()

        sys.exit(app.exec_())
