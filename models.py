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

from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QColor
from PySide2.QtSql import QSqlTableModel


class TodoModel(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.check = QImage('src/check.png')
        self.setTable('task')
        self.setEditStrategy(QSqlTableModel.EditStrategy().OnManualSubmit)
        self.setHeaderData(1, Qt.Horizontal, 'Tasks')
        self.setHeaderData(2, Qt.Horizontal, 'Status')
        self.setSort(2, Qt.AscendingOrder)
        self.select()

    def data(self, index, role):
        if index.isValid():
            row = index.row()

            if role == Qt.DecorationRole:
                status = super(TodoModel, self).data(index)
                if status == "Completed":
                    return self.check

            if role == Qt.TextColorRole:
                status = index.sibling(row, 2).data()
                if status == "Completed":
                    return QColor(Qt.darkBlue)

            if role == Qt.BackgroundColorRole:
                status = index.sibling(row, 2).data()
                if status == "Completed":
                    return QColor(Qt.white)
                else:
                    return QColor('LightGreen')

            return QSqlTableModel.data(self, index, role)
