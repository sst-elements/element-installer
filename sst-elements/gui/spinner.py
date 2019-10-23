#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implementation of a PyQt spinner

Extracted and modified from https://gist.github.com/eyllanesc/1a09157d17ba13d223c312b28a81c320
"""

from math import ceil

from PyQt5 import QtCore, QtGui, QtWidgets


class QtWaitingSpinner(QtWidgets.QWidget):

    def __init__(self, center_on_parent=True, disable_parent_when_spinning=True):

        QtWidgets.QWidget.__init__(self)

        self._center_on_parent = center_on_parent
        self._disable_parent_when_spinning = disable_parent_when_spinning

        self._color = QtGui.QColor("#95a5a6")
        self.setStyleSheet("background-color: #ecf0f1")

        self._roundness = 100.0
        self._minimum_trail_opacity = 35
        self._trail_fade_percentage = 50.0
        self._revolutions_per_second = 1.5
        self._number_of_lines = 20
        self._line_length = 10
        self._line_width = 2
        self._inner_radius = 10
        self._current_counter = 0
        self._is_spinning = False

        self.initialize()

    def initialize(self):

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.update_size()
        self.update_timer()
        self.hide()

    @QtCore.pyqtSlot()
    def rotate(self):

        self._current_counter += 1
        if self._current_counter > self._number_of_lines:
            self._current_counter = 0
        self.update()

    def update_size(self):

        size = (self._inner_radius + self._line_length) * 2
        self.setFixedSize(size, size)

    def update_timer(self):

        self.timer.setInterval(1000 / (self._number_of_lines * self._revolutions_per_second))

    def update_position(self):

        if self.parentWidget() and self._center_on_parent:
            self.move(
                self.parentWidget().width() / 2 - self.width() / 2,
                self.parentWidget().height() / 2 - self.height() / 2
            )

    @staticmethod
    def line_count_distance_from_primary(current, primary, total_num_lines):

        distance = primary - current
        if distance < 0:
            distance += total_num_lines
        return distance

    def current_line_color(self, count_distance, total_num_lines, trail_fade_perc, min_opacity, color):

        if count_distance == 0:
            return color

        min_alpha_f = min_opacity / 100.0

        distance_threshold = ceil((total_num_lines - 1) * trail_fade_perc / 100.0)

        if count_distance > distance_threshold:
            color.setAlphaF(min_alpha_f)

        else:
            alpha_diff = self._color.alphaF() - min_alpha_f
            gradient = alpha_diff / distance_threshold + 1.0
            result_alpha = color.alphaF() - gradient * count_distance
            result_alpha = min(1.0, max(0.0, result_alpha))
            color.setAlphaF(result_alpha)

        return color

    def paintEvent(self, event):

        self.update_position()

        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self._current_counter > self._number_of_lines:
            self._current_counter = 0

        painter.setPen(QtCore.Qt.NoPen)

        for i in range(self._number_of_lines):
            painter.save()
            painter.translate(
                self._inner_radius + self._line_length,
                self._inner_radius + self._line_length
            )
            rotate_angle = 360.0 * i / self._number_of_lines
            painter.rotate(rotate_angle)
            painter.translate(self._inner_radius, 0)
            distance = self.line_count_distance_from_primary(
                i, self._current_counter,
                self._number_of_lines
            )
            color = self.current_line_color(
                distance, self._number_of_lines,
                self._trail_fade_percentage, self._minimum_trail_opacity, self._color)
            painter.setBrush(color)
            painter.drawRoundedRect(
                QtCore.QRect(0, -self._line_width // 2, self._line_length, self._line_length),
                self._roundness, QtCore.Qt.RelativeSize
            )
            painter.restore()

    def start(self):

        self.update_position()
        self._is_spinning = True
        self.show()

        if self.parentWidget() and self._disable_parent_when_spinning:
            self.parentWidget().setEnabled(False)

        if not self.timer.isActive():
            self.timer.start()
            self._current_counter = 0

    def stop(self):

        self._is_spinning = False
        self.hide()

        if self.parentWidget() and self._disable_parent_when_spinning:
            self.parentWidget().setEnabled(True)

        if self.timer.isActive():
            self.timer.stop()
            self._current_counter = 0
