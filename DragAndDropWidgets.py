import PyQt5.QtWidgets
import mimetypes
import os
import time
from ML.MLManagers import MLManager_MonoValued, MLManager_MultiValued, CFG
from Animations import QRoundProgressWidget
from history_messages import HistoryMessageLeftLabel
from VideoPlayer import VideoWidget
import sys 

if sys.platform == 'win32':
    current_directory = ''.join([x + '/' for x in os.path.realpath(__file__).split('\\')[:-1]])[:-1]
else:
    current_directory = ''.join([x + '/' for x in os.path.realpath(__file__).split('/')[:-1]])[:-1]

class DragAndDropWidget_single(PyQt5.QtWidgets.QLabel):
    def __init__(self, parent, shadow = False):
        super().__init__()
        self.setAcceptDrops(True)
        self.parent = parent
        self.MLManager = MLManager_MonoValued(parent = self)
        self.MLManager.parent = self
        self.MLManager.finished.connect(self.send_history_message)
        self.prediction = str()

        if shadow:
            # set shadow to the label
            shadow = PyQt5.QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(5)
            self.setGraphicsEffect(shadow)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def mousePressEvent(self, event):
        path = self.parent.fileManager.open_file()[0]
        if path and path is not None:
            self.startAnimation()
            self.display_prediction(path)

    def is_video(self, path):
        try:
            if mimetypes.guess_type(path)[0].startswith('video'):
                return path
            else:
                PyQt5.QtWidgets.QMessageBox.warning(None, 
                                    "path does not consist the video", 
                                    f"{os.path.split(path)[1]} is not a video")
        except:
            PyQt5.QtWidgets.QMessageBox.warning(None, 
                                    "path does not consist the video", 
                                    f"{os.path.split(path)[1]} is not a video")

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file in files:
            path = self.is_video(file)
            if path and path is not None:
                self.startAnimation()
                self.display_prediction(path)
                

    @PyQt5.QtCore.pyqtSlot(str)
    def MonoValuePrediction(self, prediction):
        if not PyQt5.sip.isdeleted(self.parent.right_label):
            self.startAnimation()
            self.progress_bar.close()
            self.parent.right_label.setText(prediction)
            self.parent.right_layout.replaceWidget(self.progress_bar, self.parent.right_label)
            self.prediction = prediction

    def display_prediction(self, path):
        self.create_pbar()
        self.MLManager.PATH = path
        self.MLManager.parent = self
        self.MLManager.switch_to_MonoValue()
    
    # Start Animation
    def startAnimation(self):
        self.parent.right_layout.setCurrentIndex(0)
        if self.parent.right_layout.count() == 2:
            self.parent.right_layout.itemAt(1).widget().deleteLater()
        self.setPixmap(PyQt5.QtGui.QPixmap(f"{current_directory}/icons/checkmark.png"))
        self.parent.DropLabel_single.setText('Ждите результата...')

    # Stop Animation(According to need)
    def stopAnimation(self):
        text = 'перетащите файл \n или выберите для перевода'
        self.setPixmap(PyQt5.QtGui.QPixmap(f"{current_directory}/icons/drop_file.ico"))
        self.parent.DropLabel_single.setText(text)
    
    def create_pbar(self):
        self.progress_bar = QRoundProgressWidget()
        self.progress_bar.setObjectName('RightLabel')

        self.progress_bar.bar.setRange(0, CFG.NUM_FRAMES)
        self.progress_bar.bar.setValue(0)

        self.parent.right_label.setText('')
        self.parent.right_layout.replaceWidget(self.parent.right_label, self.progress_bar)

    def send_history_message(self):
        message = self.prediction
        filename = self.MLManager.PATH
        left_label = HistoryMessageLeftLabel(parent = self, filename = filename)
        left_label.setText(os.path.split(filename)[1])
        left_label.clicked.connect(left_label.openPlayer)
        left_label.setObjectName('LeftHistoryMessage')
        
        left_label.setAlignment(PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignHCenter)
        self.parent.left_history_layout.addWidget(left_label)

        right_label = PyQt5.QtWidgets.QLabel(message, objectName = 'RightHistoryMessage')
        right_label.setAlignment(PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignLeft)
        self.parent.right_history_layout.addWidget(right_label)
        self.stopAnimation()


class DragAndDropWidget_Multiple(PyQt5.QtWidgets.QLabel):
    def __init__(self, parent, shadow = False):
        super().__init__()
        self.setAcceptDrops(True)
        self.parent = parent
        self.MLManager = MLManager_MultiValued(parent = self)
        self.MLManager.parent = self
        self.MLManager.finished.connect(self.send_history_message)
        self.prediction = str()

        if shadow:
            # set shadow to the label
            shadow = PyQt5.QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(5)
            self.setGraphicsEffect(shadow)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def mousePressEvent(self, event):
        path = self.parent.fileManager.open_file()[0]
        if path and path is not None:
            self.startAnimation()
            self.display_prediction(path)
            # self.send_history_message(filename=self.MLManager.PATH, message=self.prediction)

    def is_video(self, path):
        try:
            if mimetypes.guess_type(path)[0].startswith('video'):
                return path
            else:
                PyQt5.QtWidgets.QMessageBox.warning(None, 
                                    "в данном пути не содержится видео", 
                                    f"{os.path.split(path)[1]} is not a video")
        except:
            PyQt5.QtWidgets.QMessageBox.warning(None, 
                                    "в данном пути не содержится видео", 
                                    f"{os.path.split(path)[1]} is not a video")

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file in files:
            path = self.is_video(file)
            if path and path is not None:
                self.startAnimation()
                self.display_prediction(path)
                

    @PyQt5.QtCore.pyqtSlot(list)
    def MonoValuePrediction(self, prediction):
        if not PyQt5.sip.isdeleted(self.parent.right_label):
            self.prediction, self.time_series = prediction
            self.progress_bar.close()
            self.parent.right_label.setText(self.prediction)
            self.parent.right_layout.replaceWidget(self.progress_bar, self.parent.right_label)

    def display_prediction(self, path):
        self.create_pbar()
        self.MLManager.PATH = path
        self.MLManager.parent = self
        self.MLManager.switch_to_MonoValue()
    
    # Start Animation
    def startAnimation(self):
        self.parent.right_layout.setCurrentIndex(0)
        self.parent.DropLabel.setText('Ждите результата...')
        self.parent.DropIcon.setPixmap(PyQt5.QtGui.QPixmap(f"{current_directory}/icons/checkmark.png"))

        try:
            self.player.deleteLater()
        except AttributeError:
            pass

    # Stop Animation(According to need)
    def stopAnimation(self):
        text = 'перетащите файл \n или выберите для перевода'
        self.parent.DropIcon.setPixmap(PyQt5.QtGui.QPixmap(f"{current_directory}/icons/drop_file.ico"))
        self.parent.DropLabel.setText(text)
    
    def create_pbar(self):
        self.progress_bar = QRoundProgressWidget()
        self.progress_bar.setObjectName('RightLabel')
        self.progress_bar.bar.setValue(0)

        self.parent.right_label.setText('')
        self.parent.right_layout.replaceWidget(self.parent.right_label, self.progress_bar)

    def add_video(self):
        self.player = VideoWidget(filename = self.MLManager.PATH, time_series=self.time_series)
        self.parent.right_layout.addWidget(self.player)
        self.parent.right_layout.setCurrentIndex(1)

    def send_history_message(self):
        message = self.prediction
        filename = self.MLManager.PATH
        self.stopAnimation()
        self.add_video()
        left_label = HistoryMessageLeftLabel(parent = self, filename = filename)
        left_label.setText(os.path.split(filename)[1])
        left_label.clicked.connect(left_label.openPlayer)
        left_label.setObjectName('LeftHistoryMessage')
        
        left_label.setAlignment(PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignHCenter)
        self.parent.left_history_layout.addWidget(left_label)

        right_label = PyQt5.QtWidgets.QLabel(message, objectName = 'RightHistoryMessage')
        right_label.setAlignment(PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignLeft)
        self.parent.right_history_layout.addWidget(right_label)
        