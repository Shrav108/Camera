import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import os
import random
import cv2


class Collector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = "ARECANUT IMAGE COLLECTION APP"
        self.setWindowTitle(self.title)

        self.select_folder_button = QtWidgets.QPushButton("Select Folder")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.select_folder_button)
        self.select_folder_button.clicked.connect(self.get_folder_name)

    def get_folder_name(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(caption='Choose Directory', directory=os.getcwd())
        self.folder_name = QtWidgets.QLabel(folder_name)
        self.layout.addWidget(self.folder_name)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = Collector()
    widget.resize(800, 600)
    widget.show()

    try:
        sys.exit(app.exec())
    except:
        print("Closing Window....")
