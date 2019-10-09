#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets

from windows import MainWindow
from templates import ColorPalette


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("SST Elements")
    # app.setStyle("Fusion")
    # app.setPalette(ColorPalette())

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
