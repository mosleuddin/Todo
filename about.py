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

from PySide2.QtGui import Qt, QFont, QPixmap, QIcon, QDesktopServices, QTextOption
from PySide2.QtCore import QUrl
from PySide2.QtWidgets import (QWidget, QDialog, QTabWidget, QPushButton, QLabel,
                               QPlainTextEdit, QVBoxLayout, QHBoxLayout, QTextBrowser, QTextEdit)

from module import init_win

# copyright_text = 'Copyright (c) 2021 Mosleuddin Sarkar'
app_name = 'Todo (1.0.0)'


class About(QDialog):
    def __init__(self, parent):
        super(About, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        win_bg = 'background-color: #afbec1'
        init_win(self, wd=.5, ht=.9, move_x=.25, move_y=.01, bg=win_bg, title='About ' + app_name)
        # Create & initialize a tab-widget and two widgets
        self.parent = parent
        self.tab_widget = QTabWidget()  # Tab widget which will contain two tabs
        self.about_app = QWidget()  # Will be used as the First Tab
        self.about_dev = QWidget()  # Will be used as the Second Tab

        self.init_tab_widget()
        self.init_about_app()
        self.init_about_dev()

        # create buttons
        button_back = QPushButton(QIcon('src/back.png'), '&Back')
        button_back.setStyleSheet(self.parent.enabled_btn_style)
        button_back.setFixedWidth(200)
        button_back.clicked.connect(self.close)

        button_website = QPushButton(QIcon('src/submit.png'), '&Website')
        button_website.setStyleSheet(self.parent.enabled_btn_style)
        button_website.setFixedWidth(200)
        button_website.clicked.connect(self.open_website)

        # layouts
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        button_layout.addSpacing(15)
        button_layout.addWidget(button_website)
        button_layout.addWidget(button_back)
        button_layout.addSpacing(15)

        main_layout.addWidget(self.tab_widget)
        main_layout.addSpacing(15)
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(10)

        self.setLayout(main_layout)

    def init_tab_widget(self):
        self.tab_widget.addTab(self.about_app, QIcon('src/todo.png'), '&Application')
        self.tab_widget.addTab(self.about_dev, QIcon('src/dev.png'), '&Developer')

    def init_about_app(self):
        # create widgets
        label_image = QLabel()
        label_image.setPixmap(QPixmap('src/todo.jpg'))

        label_app = QLabel(app_name)
        label_app.setStyleSheet("font: Arial 10 100")
        label_app.setAlignment(Qt.AlignCenter)

        self.notice = QTextBrowser()
        self.notice.setSource(QUrl('notice.html'))
        self.notice.setOpenExternalLinks(True)
        self.notice.setStyleSheet("font: Arial 12 100")
        self.notice.setFixedHeight(int(self.about_app.height() * .95))
        self.notice.setViewportMargins(10, 5, 10, 10)
        self.notice.verticalScrollBar().hide()

        self.license = QPlainTextEdit()
        text = open('LICENSE').read()
        self.license.setPlainText(text)
        self.license.setStyleSheet("background-color: rgb(222, 222, 222); font-family: Verdana; font-size:10px")
        self.license.setFixedHeight(int(self.about_app.height() * .95))
        self.license.setViewportMargins(3, 1, 1, 1)
        self.license.setReadOnly(True)
        self.license.setVisible(False)

        self.button_notice_license = QPushButton(QIcon('src/license.png'), 'Show &License')
        self.button_notice_license.setFont(QFont('Arial', 12))
        self.button_notice_license.setCheckable(True)
        self.button_notice_license.clicked.connect(self.show_notice_license)

        # layouts
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        about_main_layout = QHBoxLayout()

        # add widgets to left layout
        left_layout.addSpacing(23)
        left_layout.addWidget(label_image)

        left_layout.addWidget(label_app)
        left_layout.addStretch()

        # add widgets to button layout
        button_layout.addStretch()
        button_layout.addWidget(self.button_notice_license)

        # add widgets to right layout
        right_layout.addSpacing(20)
        right_layout.addWidget(self.notice)
        right_layout.addWidget(self.license)
        right_layout.addLayout(button_layout)

        # main layout for about_app
        about_main_layout.addLayout(left_layout)
        about_main_layout.addLayout(right_layout)
        self.about_app.setLayout(about_main_layout)

    def init_about_dev(self):
        label_image = QLabel()
        label_image.setStyleSheet('border: 4px solid #c504e6')
        label_image.setPixmap(QPixmap('src/dev.jpg'))
        label_image.setAlignment(Qt.AlignCenter)

        label_caption = QLabel('Designed and Developed by Mosleuddin Sarkar')
        label_caption.setStyleSheet('font: Arial 9 100; color: Blue')
        label_caption.setAlignment(Qt.AlignCenter)

        # layouts
        image_layout = QHBoxLayout()
        dev_main_layout = QVBoxLayout()

        image_layout.addStretch()
        image_layout.addWidget(label_image)
        image_layout.addStretch()

        dev_main_layout.addSpacing(40)
        dev_main_layout.addLayout(image_layout)
        dev_main_layout.addWidget(label_caption)
        dev_main_layout.addSpacing(30)

        self.about_dev.setLayout(dev_main_layout)

    def show_notice_license(self):
        if self.button_notice_license.isChecked():
            self.button_notice_license.setCheckable(False)
            self.notice.setVisible(False)
            self.license.setVisible(True)
            self.button_notice_license.setText('Show &Notice')
            self.button_notice_license.setIcon(QIcon('src/notice.png'))
        else:
            self.button_notice_license.setCheckable(True)
            self.notice.setVisible(True)
            self.license.setVisible(False)
            self.button_notice_license.setText('Show &License')
            self.button_notice_license.setIcon(QIcon('src/license.png'))

    def open_website(self):
        url = QUrl('https://github.com/mosleuddin/Todo.git')
        QDesktopServices.openUrl(url)
