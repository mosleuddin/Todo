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

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QDialog, QTableView, QAbstractItemView, QLabel,
                               QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from module import init_win


class MainUiWindow(QDialog):
    def __init__(self):
        super(MainUiWindow, self).__init__()
        # define stylesheet string for buttons
        self.enabled_btn_style = "width: 153; background-color: rgb(200, 200, 200);" \
                                 "font-family: Verdana, Helvetica, sans-serif;  font-size: 20px;"
        self.disabled_btn_style = "width: 153; background-color: Grey;" \
                                  "font-family: Verdana, Helvetica, sans-serif;  font-size: 20px;"

        # set values for different properties of the window
        win_width = .70  # 70% of the screen width
        win_height = .95  # 95% of the screen height
        move_x = .15  # move 15% of the screen width
        move_y = .005  # move 005% of the screen height
        win_bg = "background-color: CadetBlue"
        win_title = 'Manage Your Tasks'
        win_icon = QIcon('src/todo.png')

        init_win(self, wd=win_width, ht=win_height, move_x=move_x, move_y=move_y,
                 bg=win_bg, title=win_title, icon=win_icon)  # initialize window
        self.create_widgets()  # create required widgets for this window
        self.create_layout()  # create layout for the window and its child widgets

    def create_widgets(self):
        self.todoView = QTableView()
        self.todoView.setFixedSize(self.screen_wd * .65, self.screen_ht * .65)
        self.todoView.setStyleSheet("font-family: Verdana, Helvetica, sans-serif; font-size: 18px")
        self.todoView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.todoView.horizontalHeader().setStretchLastSection(True)
        self.todoView.setSelectionMode(QTableView.SingleSelection)
        self.todoView.setSelectionBehavior(QTableView.SelectRows)
        self.todoView.setAutoScroll(True)

        self.deleteButton = QPushButton(QIcon('src/delete.png'), '&Delete')
        self.deleteButton.setStyleSheet(self.enabled_btn_style)

        self.editButton = QPushButton(QIcon('src/edit.png'), '&Edit')
        self.editButton.setStyleSheet(self.enabled_btn_style)

        self.completeButton = QPushButton(QIcon('src/complete.png'), '&Complete')
        self.completeButton.setStyleSheet(self.enabled_btn_style)

        self.aboutButton = QPushButton(QIcon('src/about.png'), 'A&bout')
        self.aboutButton.setStyleSheet(self.enabled_btn_style)

        self.exitButton = QPushButton(QIcon('src/close.png'), 'E&xit')
        self.exitButton.setStyleSheet(self.enabled_btn_style)

        self.addButton = QPushButton(QIcon('src/add.png'), "&Add")
        self.addButton.setStyleSheet(self.enabled_btn_style)

        self.todoEdit = QLineEdit()
        self.todoEdit.setStyleSheet("background-color:BurlyWood; font-size: 20px;"
                                    " font-family: Verdana, Helvetica, sans-serif")
        self.todoEdit.setPlaceholderText('Enter new task here')

        self.pendingRecordsLabel = QLabel()
        self.pendingRecordsLabel.setStyleSheet("color: Red; font-size: 20px;"
                                               "font-family: Verdana, Helvetica, sans-serif")

        self.completedRecordsLabel = QLabel()
        self.completedRecordsLabel.setStyleSheet("color: Blue; font-size: 20px;"
                                                 "font-family: Verdana, Helvetica, sans-serif")

        self.totalRecordsLabel = QLabel()
        self.totalRecordsLabel.setStyleSheet("font-family: Verdana, Helvetica, sans-serif;"
                                             "font-size: 20px")

    def create_layout(self):
        # create layouts
        top_layout = QHBoxLayout()
        middle_layout1 = QHBoxLayout()
        middle_layout2 = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        # top layout
        top_layout.addSpacing(20)
        top_layout.addWidget(self.todoView)

        # middle layout1
        middle_layout1.addStretch()
        middle_layout1.addWidget(QLabel('Pending : '))
        middle_layout1.addWidget(self.pendingRecordsLabel)

        middle_layout1.addStretch()
        middle_layout1.addWidget(QLabel('Completed : '))
        middle_layout1.addWidget(self.completedRecordsLabel)

        middle_layout1.addStretch()
        middle_layout1.addWidget(QLabel('Total : '))
        middle_layout1.addWidget(self.totalRecordsLabel)
        middle_layout1.addStretch()

        # middle layout2
        middle_layout2.addSpacing(30)
        middle_layout2.addWidget(self.deleteButton)
        middle_layout2.addWidget(self.editButton)
        middle_layout2.addWidget(self.completeButton)
        middle_layout2.addWidget(self.aboutButton)
        middle_layout2.addWidget(self.exitButton)
        middle_layout2.addSpacing(30)

        # bottom layout
        bottom_layout.addSpacing(30)
        bottom_layout.addWidget(self.todoEdit)
        bottom_layout.addWidget(self.addButton)
        bottom_layout.addSpacing(30)

        # main layout
        main_layout.addLayout(top_layout)
        main_layout.addSpacing(15)
        main_layout.addLayout(middle_layout1)
        main_layout.addSpacing(20)
        main_layout.addLayout(middle_layout2)
        main_layout.addSpacing(20)
        main_layout.addLayout(bottom_layout)
        main_layout.addSpacing(25)
        self.setLayout(main_layout)
