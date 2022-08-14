import random
import cv2
import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from history_messages import HistoryMessageLeftLabel
import time
import os

from ML.MLManagers import MLManager_Stream, CFG


class CameraManager(PyQt5.QtCore.QThread):
    changePixmap = PyQt5.QtCore.pyqtSignal(PyQt5.QtGui.QImage)
    MLManager = MLManager_Stream()
    capture_path = None
    second_process = None
    parent = None
    capture_dims = None
    cap = None
    frames = list()
    history = None
    prompt = 'подсказка:\n' + random.choice(['держитесь по центру',
                                            'проверьте освещение',
                                             'уберите посторонних \nиз кадра'])

    def run(self):
        self.MLManager.parent = self
        self.MLManager.makePrediction.connect(self.get_prediction)
        self.cap = cv2.VideoCapture(self.capture_path, cv2.CAP_DSHOW)
        self.prediction = str()
        self.history = str()
        try:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    rgbImage = cv2.resize(rgbImage, list(
                        map(lambda a: a - 1, self.capture_dims)))
                    self.frames.append(frame)

                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = PyQt5.QtGui.QImage(
                        rgbImage.data, w, h, bytesPerLine, PyQt5.QtGui.QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(
                        self.capture_dims[0], self.capture_dims[1], PyQt5.QtCore.Qt.KeepAspectRatio)

                    if len(self.frames) == CFG.NUM_FRAMES_STREAM:
                        self.MLManager.frames = self.frames
                        self.MLManager.start()
                        self.frames = list()

                    self.changePixmap.emit(p)

        finally:
            print('released')
            self.cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.MLManager.stop()
        self._run_flag = False
        self.terminate()

    def stop_capturing(self):
        '''terminate stream thread'''
        if self.history:
            self.send_history_message()
        self.MLManager.frames = list()
        self.parent.setCameraIcon()
        if self.cap is not None:
            self.cap.release()
        self.history = ''

    @PyQt5.QtCore.pyqtSlot()
    def get_prediction(self):
        if len(self.frames) == CFG.NUM_FRAMES_STREAM:
            self.MLManager.frames = list()

    def switch_to_stream(self):
        '''activate stream mode'''
        self.changePixmap.connect(self.parent.setImage)
        self.parent.right_layout.setCurrentIndex(0)
        if self.parent.right_layout.count() == 2:
            self.parent.right_layout.itemAt(1).widget().deleteLater()
        self.start()

    def send_history_message(self):
        left_label = PyQt5.QtWidgets.QLabel('stream')
        left_label.setObjectName('LeftHistoryMessage')

        left_label.setAlignment(PyQt5.QtCore.Qt.AlignTop |
                                PyQt5.QtCore.Qt.AlignHCenter)
        self.parent.left_history_layout.addWidget(left_label)

        right_label = PyQt5.QtWidgets.QLabel(
            self.history[:-2], objectName='RightHistoryMessage')
        right_label.setAlignment(
            PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignLeft)
        self.parent.right_history_layout.addWidget(right_label)
