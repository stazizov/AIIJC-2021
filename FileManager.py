import PyQt5
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class FileManager(PyQt5.QtWidgets.QFileDialog):
    def __init__(self, parent):
        self.parent = parent
    
    def mousePressEvent(self, event):
        self.parent.fileManager.open_file()

    def open_file(self):
        '''creates window and return path of picked file'''
        FileDialog = PyQt5.QtWidgets.QFileDialog
        path = FileDialog.getOpenFileName(self.parent, 'Open a file', '',  "Video Files (*.mp4 *.avi *.MOV *.WMV *.MKV)", )
        return path