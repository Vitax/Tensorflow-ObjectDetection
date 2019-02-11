""" Class to create a QT Window which will contain all elements needed to display
    the Object Detection done in Tensorflow
    __author__ = "Caglar Özel"
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from gui.gui_elements.menu_bar import menu_bar
from gui.gui_elements import main_section


class Window(QMainWindow):
    ''' Class of the Window '''

    def __init__(self):
        super().__init__()

        self.setMinimumSize(1024, 768)

        self.widget = QWidget()
        self.app_layout = QVBoxLayout()

        self.width, self.height = self.widget.width(), self.widget.height()

        # Create components of the application and add it to the app_layout
        self.main_menu = menu_bar.MenuBar()
        self.main_section = main_section.MainSection()

        self.app_layout.addLayout(self.main_menu)
        self.app_layout.addLayout(self.main_section)

        self.widget.setWindowTitle("Tensorflow Object Detection Client")
        self.widget.setLayout(self.app_layout)
        self.setCentralWidget(self.widget)

    def resizeEvent(self, event):
        """ Override resize event method of Qt """
        QMainWindow.resizeEvent(self, event)

        self.width = self.widget.width()
        self.height = self.widget.height()

        self.main_section.resize_update(self.width, self.height)

    def draw(self):
        ''' Execute the create PyQt5 Application '''
        self.show()
