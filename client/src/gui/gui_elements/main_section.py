"""Class to create the Side Section of the Application which will cover
   the List of Image contained in a Folder and the Logic to choose it

    __author__ = "Caglar Özel"
"""

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget, QTabWidget

from gui.gui_elements.image_section import image_section
from gui.gui_elements.camera_section import camera_section


class MainSection(QVBoxLayout):
    ''' Class of the MainSection '''

    def __init__(self):
        super().__init__()

        self.img_widget = QWidget()
        self.image_section_layout = image_section.ImageSection()
        self.img_widget.setLayout(self.image_section_layout)

        self.camera_widget = QWidget()
        self.camera_section_layout = camera_section.CameraSection()
        self.camera_widget.setLayout(self.camera_section_layout)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.img_widget, "Images")
        self.tabs.addTab(self.camera_widget, "Camera")

        self.addWidget(self.tabs)

    def resize_update(self, width, height):
        """ resize_update function """
        self.image_section_layout.resize_update(width, height)
        self.camera_section_layout.resize_update(width, height)
