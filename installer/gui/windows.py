#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import installer
import os
from .templates import SSTElementWindow, SplashScreen, ElementsListWindow

# suppress all console outputs
installer.LOG = False


class CustomSpinBox(QtWidgets.QSpinBox):
    def __init__(self, *args, **kwargs):
        super(CustomSpinBox, self).__init__(*args, **kwargs)

    def textFromValue(self, value):
        return "Max" if value == self.maximum() else str(value)

class ElementOptionsWindow(SSTElementWindow):

    def __init__(self, parent):

        self.parent = parent
        super(ElementOptionsWindow, self).__init__(self.parent)

        self.element = None

        self.install_btn = None
        self.uninstall_btn = None
        self.tests_btn = None

        self.gen_label = None
        self.gen_btns = []
        self.gen_chosen = "makefile"
        self.gen_group = None

        self.jobs_spin_box = None
        self.jobs = 0
        self.__max_jobs = 0

        self.add_header()

        self.url = QtWidgets.QLabel()
        self.url.setOpenExternalLinks(True)
        self.insert_widget(self.url)

        self.about = QtWidgets.QTextEdit()
        self.about.setReadOnly(True)
        self.insert_widget(self.about)

        self.add_back_btn()
        self.add_exit_btn()
        self.add_hlayout()

    def set_element(self, element):

        self.element = element
        readme, url = installer.get_info(self.element)
        self.url.setText(f"<a href='{url}'>{url}</a>")
        self.about.setText(readme)

    def set_registered(self, registered):

        # if element is registered, replace the install button with the uninstall button
        if registered:

            self.set_header(f"{self.element}<font color='#27ae60'> ✓</font>")
            if not self.uninstall_btn:

                # tests button
                self.tests_btn = QtWidgets.QPushButton("Tests")
                self.tests_btn.clicked.connect(
                    lambda: self.element_tests_action(self.element))
                self.insert_widget(self.tests_btn, 3)

                # uninstall button
                self.uninstall_btn = QtWidgets.QPushButton("Uninstall")
                self.uninstall_btn.clicked.connect(
                    lambda: self.element_action(installer.uninstall))
                self.insert_widget(self.uninstall_btn, 4)
                self.uninstall_btn.setStyleSheet("background-color: #e74c3c")

            if self.install_btn:

                self.install_btn.deleteLater()
                self.install_btn = None

                self.gen_label.deleteLater()
                for gen_btn in self.gen_btns:
                    gen_btn.deleteLater()
                    gen_btn = None

                self.gen_label = None

                self.jobs_check.deleteLater()
                self.jobs_check = None

                if self.jobs_spin_box:
                    self.jobs_spin_box.deleteLater()
                    self.jobs_spin_box = None

        # replace the uninstall button with the install button
        else:

            self.set_header(f"{self.element}")
            if not self.install_btn:

                # generator sub-layout
                self.__gen_sub_layout = QtWidgets.QHBoxLayout()

                self.gen_label = QtWidgets.QLabel("Choose your build tool:")
                for gen in ("Makefile", "Ninja"):
                    self.gen_btns.append(QtWidgets.QRadioButton(gen))
                self.gen_group = QtWidgets.QButtonGroup()

                self.gen_btns[0].setChecked(True)
                for gen_btn in self.gen_btns:
                    self.gen_group.addButton(gen_btn)
                    gen_btn.toggled.connect(self.on_checked_gen)

                self.__gen_sub_layout.addWidget(self.gen_label)
                for gen_btn in self.gen_btns:
                    self.__gen_sub_layout.addWidget(gen_btn)

                self.add_sub_layout(self.__gen_sub_layout, 3)

                # jobs sub-layout
                self.__jobs_sub_layout = QtWidgets.QHBoxLayout()
                self.jobs_check = QtWidgets.QRadioButton("Enable parallel builds")
                self.jobs_check.toggled.connect(self.on_checked_jobs)

                self.__jobs_sub_layout.addWidget(self.jobs_check)
                self.add_sub_layout(self.__jobs_sub_layout, 4)

                # install button
                self.install_btn = QtWidgets.QPushButton("Install")
                self.install_btn.clicked.connect(
                    lambda: self.element_action(installer.install, generator=self.gen_chosen,
                                                n_jobs=self.jobs))
                self.insert_widget(self.install_btn, 5)
                self.install_btn.setStyleSheet("background-color: #27ae60")

            if self.uninstall_btn:

                self.uninstall_btn.deleteLater()
                self.tests_btn.deleteLater()
                self.uninstall_btn = None
                self.tests_btn = None

    def element_tests_action(self, element_name):

        installer.list_tests(element_name)

    def on_spin_jobs(self, value):

        self.jobs = 0 if value == self.__max_jobs else value

    def _update_jobs(self):

        if self.jobs_spin_box:

            cores = os.cpu_count() + 1

            if self.gen_chosen == "makefile":
                self.__max_jobs = cores
                self.jobs_spin_box.setMaximum(self.__max_jobs)
                self.jobs_spin_box.setValue(self.__max_jobs)

            elif self.gen_chosen == "ninja":
                self.__max_jobs = cores + 2
                self.jobs_spin_box.setMaximum(self.__max_jobs)
                self.jobs_spin_box.setValue(self.__max_jobs)

    def on_checked_gen(self):

        radio_btn = self.sender()
        if radio_btn.isChecked():
            self.gen_chosen = radio_btn.text().lower()
            self._update_jobs()

    def on_checked_jobs(self):

        if self.sender().isChecked():
            self.jobs_spin_box = CustomSpinBox()
            self.jobs_spin_box.setMinimum(1)
            self.jobs_spin_box.setStepType(1)
            self.jobs_spin_box.valueChanged.connect(self.on_spin_jobs)
            self._update_jobs()

            self.__jobs_sub_layout.addWidget(self.jobs_spin_box)

        else:
            self.jobs_spin_box.deleteLater()
            self.jobs_spin_box = None

    def element_action(self, action, **action_args):

        splash = SplashScreen(self, self.element, action, **action_args)
        splash.setWindowModality(QtCore.Qt.ApplicationModal)
        splash.show()

    def update(self, rdata):

        self.set_registered(not rdata)
        self.parent.update()


class RegisteredElementsWindow(ElementsListWindow):

    def __init__(self, parent):

        super(RegisteredElementsWindow, self).__init__(parent, header="Registered Elements")
        self.selected_element_window = ElementOptionsWindow(self)

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        self.hide()
        self.selected_element_window.set_element(self.elements[index.row()])
        self.selected_element_window.set_registered(True)
        self.selected_element_window.show()

    def update(self):

        self.list_view.clear()
        self.elements = installer.list_registered_elements()
        for element in self.elements:
            element_item = QtWidgets.QListWidgetItem(element)
            element_item.setSelected(False)
            element_item.setIcon(self.default_icon)
            self.list_view.addItem(element_item)


class ElementsWindow(ElementsListWindow):

    def __init__(self, parent):

        super(ElementsWindow, self).__init__(parent, header="SST Elements")
        self.selected_element_window = ElementOptionsWindow(self)

    @QtCore.pyqtSlot("QModelIndex")
    def on_list_view_clicked(self, index):

        element = self.elements[index.row()]
        self.hide()
        self.selected_element_window.set_element(element)
        self.selected_element_window.set_registered(installer.is_registered(element))
        self.selected_element_window.show()

    def update(self):

        self.list_view.clear()
        self.elements = list(installer.list_all_elements().keys())
        for element in self.elements:
            element_item = QtWidgets.QListWidgetItem(element)
            if installer.is_registered(element):
                element_item.setBackground(QtGui.QColor("#2ecc71"))
            element_item.setSelected(False)
            element_item.setIcon(self.default_icon)
            self.list_view.addItem(element_item)


class MainWindow(SSTElementWindow):

    def __init__(self):

        super(MainWindow, self).__init__(None)

        self.intro = QtWidgets.QTextEdit()
        self.intro.setReadOnly(True)
        self.intro.setText(f"""
            <h1>SST Elements</h1>
            <p style='font-size:12px;text-align:center'>{installer.get_version()}</p>
        """)
        self.intro.setAlignment(QtCore.Qt.AlignCenter)
        self.intro.setStyleSheet("padding-top: 175")
        self.insert_widget(self.intro)

        reg_elems_btn = QtWidgets.QPushButton("Registered elements")
        self.insert_widget(reg_elems_btn)

        install_elems_btn = QtWidgets.QPushButton("New elements")
        self.insert_widget(install_elems_btn)

        self.add_exit_btn()
        self.add_hlayout()

        reg_elems_btn.clicked.connect(self.on_list_elems_clicked)
        install_elems_btn.clicked.connect(self.on_install_elems_clicked)

        self.elements_window = ElementsWindow(self)
        self.registered_elements_window = RegisteredElementsWindow(self)

    def on_list_elems_clicked(self):

        self.hide()
        self.registered_elements_window.update()
        self.registered_elements_window.show()

    def on_install_elems_clicked(self):

        self.hide()
        self.elements_window.update()
        self.elements_window.show()
