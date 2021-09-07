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
from PySide2.QtGui import QIcon
from PySide2.QtSql import QSqlRecord
from PySide2.QtWidgets import (QDialog, QLabel, QLineEdit, QComboBox, QPushButton,
                               QVBoxLayout, QHBoxLayout, QFormLayout)
from module import init_win, info


class EditTask(QDialog):
    def __init__(self, parent, curr_row, curr_task, curr_status):
        super(EditTask, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        # set values for different properties of the window
        win_width = .50  # 50% of the width of the screen
        win_height = .40  # 40% of the width of the screen
        win_move_width = .25  # 25% of the width of the screen
        win_move_height = .15  # 15% of the height of the screen
        win_bg = "background-color: Grey"
        win_icon = QIcon('src/todo.png')
        win_title = 'Edit Task'

        self.parent = parent
        self.curr_row = curr_row
        self.curr_task = curr_task
        self.curr_status = curr_status

        init_win(self, wd=win_width, ht=win_height, move_x=win_move_width, move_y=win_move_height,
                 bg=win_bg, title=win_title, icon=win_icon)  # initialize window
        self.create_widgets()  # create required widgets for this window

        self.taskEdit.textChanged.connect(self.data_changed)
        self.statusCombo.currentTextChanged.connect(self.data_changed)
        self.cancelButton.pressed.connect(self.cancel)
        self.submitButton.pressed.connect(self.submit)

    def create_widgets(self):
        edit_style = "background-color: rgb(75, 180, 145); font-family: Helvetica, Verdana," \
                     " sans-serif; font-size: 20px; "
        label_style = "font-family: Helvetica, Verdana, sans-serif; font-size: 20px;"

        self.taskLabel = QLabel('&Task')
        self.taskLabel.setStyleSheet(label_style)

        self.taskEdit = QLineEdit()
        self.taskEdit.setStyleSheet(edit_style)
        self.taskEdit.setText(self.curr_task)

        self.statusLabel = QLabel('&Status')
        self.statusLabel.setStyleSheet(label_style)

        self.statusCombo = QComboBox()
        self.statusCombo.setFixedWidth(125)
        self.statusCombo.setStyleSheet(edit_style)
        self.statusCombo.addItems(['Pending', 'Completed'])
        self.statusCombo.setCurrentText(self.curr_status)

        self.taskLabel.setBuddy(self.taskEdit)
        self.statusLabel.setBuddy(self.statusCombo)

        self.cancelButton = QPushButton(QIcon('src/back.png'), "&Cancel")
        self.cancelButton.setStyleSheet(self.parent.enabled_btn_style)

        self.submitButton = QPushButton(QIcon('src/submit.png'), "Su&bmit")
        self.submitButton.setEnabled(False)
        self.submitButton.setStyleSheet(self.parent.disabled_btn_style )

        # layouts
        form_layout = QFormLayout()
        button_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(20)
        form_layout.setMargin(15)
        form_layout.addRow(self.taskLabel, self.taskEdit)
        form_layout.addRow(self.statusLabel, self.statusCombo)

        button_layout.addStretch()
        button_layout.addWidget(self.cancelButton)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.submitButton)
        button_layout.addStretch()

        main_layout.addSpacing(10)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(40)
        self.setLayout(main_layout)

    def data_changed(self):
        self.submitButton.setEnabled(True)
        self.submitButton.setStyleSheet(self.parent.enabled_btn_style )

    def submit(self):
        task = self.taskEdit.text().strip()
        status = self.statusCombo.currentText()
        if len(task) > 0:
            record = QSqlRecord(self.parent.model.record(self.curr_row))
            record.setValue('task', task)
            record.setValue('status', status)
            self.parent.model.setRecord(self.curr_row, record)
            self.parent.model.submitAll()
            self.parent.updateTotals()
            self.close()
        else:
            info(self, 'Attention!', 'Task can not be left blank')
            self.taskEdit.setText(self.curr_task)
            self.taskEdit.setFocus()

    def cancel(self):
        self.close()
