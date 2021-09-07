"""
    Copyright (c) 2021  Mosleuddin Sarkar

    This file is part of Todo.

    Todo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Todo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Todo.  If not, see <https://www.gnu.org/licenses/>.
"""

from PySide2.QtWidgets import QApplication, QMessageBox


def init_win(self, wd=500, ht=500, move_x=0, move_y=0,
             bg="background-color: White", title="", icon=None):
    geometry = QApplication.desktop().availableGeometry(self)
    self.screen_wd = geometry.width()
    self.screen_ht = geometry.height()
    self.setFixedSize(self.screen_wd * wd, self.screen_ht * ht)
    self.move(int(self.screen_wd * move_x), int(self.screen_wd * move_y))
    self.setStyleSheet(bg)
    self.setWindowTitle(title)
    if icon is not None:
        self.setWindowIcon(icon)


def info(self, title, msg):
    QMessageBox.information(self, title, msg)
    return


def warn(self, title, msg):
    response = QMessageBox.warning(self, title, msg, QMessageBox.Yes, QMessageBox.No)
    if response == QMessageBox.Yes:
        return True
    else:
        return False


def confirm(self, title, msg):
    response = QMessageBox.question(self, title, msg, QMessageBox.Yes, QMessageBox.No)
    if response == QMessageBox.Yes:
        return True
    else:
        return False


"""
def image_path(path_to_image):
    bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
    return path.abspath(path.join(bundle_dir, path_to_image))
"""
