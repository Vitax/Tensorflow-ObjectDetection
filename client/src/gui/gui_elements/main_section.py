"""Class to create the Side Section of the Application which will cover
   the List of Image contained in a Folder and the Logic to choose it

    __author__ = "Caglar Özel"
"""

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton

from gui.gui_elements import image_section
from gui.gui_elements.common import file_manager


class MainSection(QHBoxLayout):
    ''' Class of the MainSection '''

    def __init__(self):
        super().__init__()

        self.chosen_image_directory = ""

        self.tree_obj = None
        self.image_section = None
        self.file_manager = file_manager.FileManager(250)
        self.image_section = image_section.ImageSection()
        self.image_section.addStretch(1)

        self.tree_view_layout = QVBoxLayout()
        self.tree_view_layout.setAlignment(Qt.AlignLeft)

        button = QPushButton()
        button.setText('Open Folder')
        button.clicked.connect(
            lambda x: self.file_manager.create_tree_view_popup("", self.set_image_dir, True)
        )

        self.tree_view_layout.addWidget(button)

        self.tree_obj = self.file_manager.create_tree_view("/home", self.get_selected_media)
        self.tree_view_layout.addWidget(self.tree_obj["file_manager"])

        self.addLayout(self.tree_view_layout)
        self.addLayout(self.image_section)

    def resize_update(self, width, height):
        """ resize_update function """
        self.image_section.resize_update(width, height)

    def set_image_dir(self, chosen_dir):
        """ Set the side view with the chosen directory """
        self.chosen_image_directory = chosen_dir["dir_path"]
        self.tree_obj["file_manager"].setRootIndex(
            self.tree_obj["file_model"].index(chosen_dir["dir_path"])
        )

    def get_selected_media(self, chosen_item):
        """ return the selected item from the side section """
        self.image_section.show_media(chosen_item["file_path"])
