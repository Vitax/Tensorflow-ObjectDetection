""" Main to run the Application """

import sys

from gui import window
from PyQt5.QtWidgets import QApplication


def main():
    """ Main function to start the Application """
    app = QApplication(sys.argv)

    gui_window = window.Window()
    gui_window.draw()

    app.exec_()


if __name__ == "__main__":
    main()
