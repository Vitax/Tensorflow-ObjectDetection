""" This class will create the MenuBar section at the top of the Application
    which will enable the user to setup which inference graph etc. to use
    to perform the object detection.

    ___author___ = "Caglar Özel"
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QMenuBar, QAction, QWidget, QLineEdit, QPushButton, QLabel

from gui.gui_elements.common import file_manager
from helper import config_getter


class MenuBar(QVBoxLayout):
    """ Class of the MenuBar

    params:
    -------
    config_file_path: File
        Path to the configuration file where the path's to the tensorflow items will be stored
    inference_graph_path: string
        Path of the inference graph used by the tensorfow model
    label_map_path: string
        Path to the label map used by the tensorflow model
    num_classes: int
        Number of classes trained and detected by the label map and inference graph
    inference_graph_line: QLineEdit
        Global private variable used to change content in functions
    label_map_line: QLineEdit
        Global private variable used to change content in functions
    """

    def __init__(self):
        super().__init__()

        self.inference_graph_path = ""
        self.label_map_path = ""
        self.num_classes = str(0)

        self.get_config_content()

        self.file_manager = file_manager.FileManager()
        self.menu_bar = QMenuBar()

        self.config_action = QAction('&Configuration')
        self.config_action.setShortcut("Ctrl-Shift+Q")
        self.config_action.setStatusTip("Setup Configuration files")
        self.config_action.triggered.connect(self.config_button_clicked)

        self.edit_option = self.menu_bar.addMenu('&Edit')
        self.edit_option.addAction(self.config_action)

        self.addWidget(self.menu_bar)

    def get_config_content(self):
        self.config_file_path = config_getter.get_config_file()
        content = config_getter.get_config_file_content(self.config_file_path)

        if content is not None:
            self.inference_graph_path = content["inference_graph"]
            self.label_map_path = content["label_map"]
            self.num_classes = content["num_classes"]
        else:
            self.inference_graph_path = ""
            self.label_map_path = ""
            self.num_classes = str(0)

    def config_button_clicked(self):
        """ Event function for the config button """
        self.popup_window = QWidget()

        popup_layout = self.config_rows()

        self.popup_window.setLayout(popup_layout)
        self.popup_window.show()

    def header_layout(self):
        """ Header layout which contains the header """
        header_layout = QVBoxLayout()

        header = QLabel()
        header.setText("Configuration")
        header.setStyleSheet("font: bold 18pt")
        header.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(header)

        return header_layout

    def button_layout(self):
        """ Button Layout of the configration window """
        button_layout = QHBoxLayout()

        save_button = QPushButton()
        save_button.setText("Save Settings")
        save_button.clicked.connect(self.save_config)

        close_button = QPushButton()
        close_button.setText("Close")
        close_button.clicked.connect(self.close_config)

        button_layout.addStretch(1)
        button_layout.addWidget(save_button)
        button_layout.addWidget(close_button)

        return button_layout

    def config_rows(self):
        """ Returns a Layout of all configuration Rows """
        popup_layout = QVBoxLayout()
        header_layout = self.header_layout()
        button_layout = self.button_layout()

        row_1 = self.config_row_inference_graph("Inference Graph:", "Browse")
        row_2 = self.config_row_label_map("Label Map:", "Browse")
        row_3 = self.config_row_num_classes("Number of Classes:")

        popup_layout.addLayout(header_layout)
        popup_layout.addLayout(row_1)
        popup_layout.addLayout(row_2)
        popup_layout.addLayout(row_3)
        popup_layout.addLayout(button_layout)

        return popup_layout

    def save_config(self):
        """ Function to save the chosen paths into a and number of classes into a config file """
        config_file = open(self.config_file_path, 'w')
        config_file.write('{ \n')
        config_file.write('\t"inference_graph": "' + self.inference_graph_line.text() + '" , \n')
        config_file.write('\t"label_map": "' + self.label_map_line.text() + '", \n')
        config_file.write('\t"num_classes": "' + self.num_classes_line.text() + '" \n')
        config_file.write('}')

        config_file.close()
        self.close_config()

    def close_config(self):
        """ Function to close the open popup window """
        self.popup_window.close()

    def config_row_inference_graph(self, line_label, button_label):
        """ Represents the Inference Graph row in the configuration window """
        row = QHBoxLayout()

        config_label = QLabel()
        config_label.setText(line_label)

        config_line = QLineEdit()
        config_line.setText(self.inference_graph_path)
        self.inference_graph_line = config_line

        row.addWidget(config_label)
        row.addWidget(config_line)

        browse_button = QPushButton()
        browse_button.setText(button_label)
        browse_button.clicked.connect(self.browse_button_inference_graph_clicked)
        row.addWidget(browse_button)

        return row

    def browse_button_inference_graph_clicked(self):
        """ Function which gets called on inference_graph button click """
        self.file_manager.create_tree_view_popup(
            self.inference_graph_path, self.callback_func_inference_graph
        )

    def callback_func_inference_graph(self, value):
        """ Callback which receives the value of the selected element in the TreeView instance """
        self.inference_graph_line.setText(value["file_path"])
        self.inference_graph_path = value["file_path"]

    def config_row_label_map(self, line_label, button_label):
        """ Represents the Label Map row in the configuration window """
        row = QHBoxLayout()

        config_label = QLabel()
        config_label.setText(line_label)

        config_line = QLineEdit()
        config_line.setText(self.label_map_path)
        self.label_map_line = config_line

        row.addWidget(config_label)
        row.addWidget(config_line)

        browse_button = QPushButton()
        browse_button.setText(button_label)
        browse_button.clicked.connect(self.browse_button_label_map_clicked)
        row.addWidget(browse_button)

        return row

    def config_row_num_classes(self, line_label):
        """ Represents the Number of Classes row in the configuration window """
        row = QHBoxLayout()

        config_label = QLabel()
        config_label.setText(line_label)

        config_line = QLineEdit()
        config_line.setText(self.num_classes)
        self.num_classes_line = config_line

        row.addWidget(config_label)
        row.addWidget(config_line)

        return row

    def browse_button_label_map_clicked(self):
        """ Function which gets called on label_map button click """
        self.get_config_content()
        self.file_manager.create_tree_view_popup(self.label_map_path, self.callback_func_label_map)

    def callback_func_label_map(self, value):
        """ Callback which receives the value of the selected element in the TreeView instance """
        self.label_map_line.setText(value["file_path"])
        self.label_map_path = value["file_path"]
