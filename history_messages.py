import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from VideoPlayer import VideoPlayer

class HistoryMessageLeftLabel(PyQt5.QtWidgets.QLabel):
    clicked = PyQt5.QtCore.pyqtSignal()
    def __init__(self, filename, parent=None):
        PyQt5.QtWidgets.QLabel.__init__(self, parent=parent)
        self.parent = parent
        self.filename = filename

    def mousePressEvent(self, event):
        self.clicked.emit()
    
    def openPlayer(self):
        self.parent.player = VideoPlayer(filename = self.filename)
        self.parent.player.show()
    
    