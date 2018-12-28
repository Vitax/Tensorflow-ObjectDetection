""" This class is responsible to either create a TreeView and display it in place
    or to create a TreeView which will be displayed in an external window
"""
import os

from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileDialog


class FileManager:
    """ Create a popup window to select a folder / file

    Global Varables
    ---------------
    item_index:
        PyQt5 index element to have a global reference to currently clicked element
    callback_func:
        Global reference to set the callback function passed into create_tree_view_popup
    popup_window:
        Global reference to the QWidget window which serves as a popup container for the TreeView

    """

    # pylint: disable=no-self-use

    def __init__(self, width=0):
        """ Initializes required variables by the class """
        self.width = width

        self.item_index = None
        self.callback_func = None
        self.popup_window = None
        self.model = None

    def create_tree_view(self, start_path="/home", callback=None):
        """ Display the tree view to choose a folder """
        file_manager = QTreeView()
        self.callback_func = callback

        self.model = QFileSystemModel()
        self.model.setRootPath(start_path)

        # for ViewType in (QColumnView, QTreeView):
        file_manager.setModel(self.model)

        # hide all columns except the filename
        for i in range(1, self.model.columnCount()):
            file_manager.hideColumn(i)

        file_manager.setRootIndex(self.model.index(start_path))
        file_manager.setFixedWidth(self.width)

        file_manager.clicked.connect(self.item_clicked)
        return {"file_manager": file_manager, "file_model": self.model}

    def create_file_dialog(self, start_path="/home"):
        """ Create a file dialog window """
        file_dialog = QFileDialog()

        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setDirectory(start_path)

        return file_dialog

    def create_tree_view_popup(self, start_path="/home", callback=None, directory=False):
        """ Function which creates a TreeView in a external Window"""
        # self.popup_window = QWidget()
        actual_path = None

        if not os.path.isdir(start_path) and os.path.isfile(start_path):
            path_arr = start_path.split('/')
            path_arr.pop(len(path_arr) - 1)
            actual_path = '/'.join(e for e in path_arr)
        else:
            actual_path = "/home"

        if not directory:
            filename = QFileDialog.getOpenFileName(None, "Open File", actual_path)
            if filename[0]:
                callback({"file_path": filename[0]})
        else:
            directory = QFileDialog.getExistingDirectory(
                None, 'Select a Folder:', actual_path, QFileDialog.ShowDirsOnly
            )
            callback({"dir_path": directory})

    def item_clicked(self, index):
        """ Helper function to keep track of the selected item in the TreeView """
        self.item_index = index
        self.select_item()

    def select_item(self):
        """ Passes the current selected item to the callback function and closes the window """
        # get the index of the currently chosen item
        index_item = self.model.index(self.item_index.row(), 0, self.item_index.parent())
        # get the file path of this item
        file_path = self.model.filePath(index_item)
        # return it with a callback
        self.callback_func({"file_path": file_path})
