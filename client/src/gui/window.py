""" Class to create a QT Window which will contain all elements needed to display
    the Object Detection done in Tensorflow
    __author__ = "Caglar Özel"
"""

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from gui.gui_elements import menu_bar, main_section


class Window(QMainWindow):
    ''' Class of the Window '''

    def __init__(self):
        super().__init__()

        self.widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.width, self.height = self.widget.width(), self.widget.height()

        # Create components of the application and add it to the main_layout
        self.main_menu = menu_bar.MenuBar()
        self.main_section = main_section.MainSection()

        self.main_layout.addLayout(self.main_menu)
        self.main_layout.addLayout(self.main_section)

        self.widget.setWindowTitle("Tensorflow Object Detection Client")
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    def resizeEvent(self, event):
        """ Override resize event method of Qt """
        QMainWindow.resizeEvent(self, event)

        self.width = self.widget.width()
        self.height = self.widget.height()

        debounce = QTimer()
        debounce.setInterval(250)
        debounce.setSingleShot(True)
        debounce.timeout.connect(self.resizeEvent)

        self.main_section.resize_update(self.width, self.height)

    def draw(self):
        ''' Execute the create PyQt5 Application '''
        self.show()
