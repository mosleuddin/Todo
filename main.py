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

import sys
from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord
from PySide2.QtWidgets import QApplication, QLabel

from main_ui import MainUiWindow
from models import TodoModel
from module import info, warn, confirm
from edit import EditTask
from about import About


class Main(MainUiWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.text_label = QLabel(self)
        self.image_label = QLabel(self)
        self.connectDB()

        self.model = TodoModel()
        self.updateTotals()

        if self.model.rowCount():
            self.show_task()
        else:
            self.no_task()

        self.aboutButton.pressed.connect(self.onAbout)
        self.addButton.pressed.connect(self.onAdd)
        self.editButton.pressed.connect(self.onEdit)
        self.deleteButton.pressed.connect(self.onDelete)
        self.completeButton.pressed.connect(self.onComplete)
        self.exitButton.pressed.connect(self.close)

    def show_task(self):
        self.image_label.hide()
        self.text_label.hide()
        self.enable_buttons()
        self.todoView.setModel(self.model)
        self.todoView.hideColumn(0)
        self.todoView.setColumnWidth(1, self.todoView.width() * .78)
        self.todoEdit.setFocus()

    def no_task(self):
        self.disable_buttons()

        width = self.todoView.width()
        height = self.todoView.height()

        self.image_label.setPixmap('src/no_task.png')
        self.image_label.setGeometry(int(width / 2.2), height / 8, int(width / 2.4), height / 2)

        self.text_label.setText("<h1>No Task</h1>")
        self.text_label.setStyleSheet("font: Arial; color: rgb(255, 0, 0)")
        self.text_label.setGeometry(width/2, int(height/1.7), width/2, int(height/3))

        self.image_label.show()
        self.text_label.show()

    def enable_buttons(self):
        self.deleteButton.setStyleSheet(self.enabled_btn_style)
        self.editButton.setStyleSheet(self.enabled_btn_style)
        self.completeButton.setStyleSheet(self.enabled_btn_style)

        self.deleteButton.setEnabled(True)
        self.editButton.setEnabled(True)
        self.completeButton.setEnabled(True)

    def disable_buttons(self):
        self.deleteButton.setStyleSheet(self.disabled_btn_style)
        self.editButton.setStyleSheet(self.disabled_btn_style)
        self.completeButton.setStyleSheet(self.disabled_btn_style)

        self.deleteButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.completeButton.setEnabled(False)

    def connectDB(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("src/todo.db")
        if self.db.open():
            myQuery = QSqlQuery()
            myQuery.exec_("""CREATE TABLE IF NOT EXISTS task(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                 task CHAR(30) NOT NULL,
                                 status CHAR(15))""")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        response = confirm(self, 'Confirm Exit', 'Are you sure you want to exit?')
        if response:
            self.db.close()
            self.db.setDatabaseName("")
            QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())
            event.accept()
        else:
            event.ignore()
            self.todoView.clearSelection()
            self.todoEdit.setFocus()

    def onAdd(self):
        task = self.todoEdit.text().strip()
        status = 'Pending'
        if len(task) > 0:
            row = self.model.rowCount()
            self.model.insertRows(row, 1)
            self.model.setData(self.model.index(row, 1), task)
            self.model.setData(self.model.index(row, 2), status)
            self.model.submitAll()
            self.updateTotals()
            if self.model.rowCount() == 1:  # if first record inserted
                self.show_task()
        else:
            info(self, 'Attention!', 'Please enter new task')

        self.todoEdit.setText('')
        self.todoEdit.setFocus()

    def onDelete(self):
        selected = self.todoView.selectedIndexes()
        if selected:
            response = warn(self, 'Confirm Delete!', 'Do you want to delete the selected task?')
            if response:
                current_index = self.todoView.currentIndex()
                current_row = current_index.row()
                self.model.removeRows(current_row, 1)
                self.model.submitAll()
                self.updateTotals()
                if self.model.rowCount() == 0:  # After deletion, if no record exists
                    self.no_task()
        else:
            info(self, 'Attention!', 'Please select a task to delete')

        self.todoView.clearSelection()
        self.todoEdit.setFocus()

    def onComplete(self):
        selected = self.todoView.selectedIndexes()
        if selected:
            current_index = self.todoView.currentIndex()
            current_row = current_index.row()
            current_record = QSqlRecord(self.model.record(current_row))
            current_status = current_record.value('status')
            if current_status != 'Completed':
                current_record.setValue('status', 'Completed')
                self.model.setRecord(current_row, current_record)
                self.model.submitAll()
                self.updateTotals()
            else:
                info(self, 'Attention!', 'This task is already completed')
        else:
            info(self, 'Attention!', 'Please select a task to complete')

        self.todoView.clearSelection()
        self.todoEdit.setFocus()

    def onEdit(self):
        selected = self.todoView.selectedIndexes()
        if selected:
            current_index = self.todoView.currentIndex()
            current_row = current_index.row()
            current_record = QSqlRecord(self.model.record(current_row))
            current_task = current_record.value('task')
            current_status = current_record.value('status')

            dlg = EditTask(self, current_row, current_task, current_status)
            dlg.show()
        else:
            info(self, 'Attention!', 'Please select a task to edit')

        self.todoView.clearSelection()
        self.todoEdit.setFocus()

    def updateTotals(self):
        pending_records = 0
        completed_records = 0
        rows = self.model.rowCount()
        for row in range(rows):
            record = self.model.record(row)
            status = record.field(2).value()
            if status == "Completed":
                completed_records += 1
            elif status == "Pending":
                pending_records += 1

        self.pendingRecordsLabel.setText(str(pending_records))
        self.completedRecordsLabel.setText(str(completed_records))
        self.totalRecordsLabel.setText(str(rows))

    def onAbout(self):
        dlg = About(self)
        dlg.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    app.exec_()
    sys.exit()
