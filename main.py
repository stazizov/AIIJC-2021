import os
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *
import sys
from stylesheets import StyleSheetsManager
from FileManager import FileManager
from DragAndDropWidgets import DragAndDropWidget_single, DragAndDropWidget_Multiple
from Camera_Manager import CameraManager
import random

if sys.platform == 'win32':
    current_directory = ''.join(
        [x + '/' for x in os.path.realpath(__file__).split('\\')[:-1]])[:-1]
else:
    current_directory = ''.join(
        [x + '/' for x in os.path.realpath(__file__).split('/')[:-1]])[:-1]


class Window(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.styleManager = StyleSheetsManager(parent=self)
        self.fileManager = FileManager(parent=self)
        self.cameraManager = self.BuildCameraManager()
        self.CreateGUI()
        self.styleManager.setStyle(mode=True)

    def BuildCameraManager(self):
        cameraManager = CameraManager(parent=self)
        cameraManager.parent = self
        cameraManager.capture_path = 0
        cameraManager.capture_dims = (640, 480)
        return cameraManager

    @QtCore.pyqtSlot(PyQt5.QtGui.QImage)
    def setImage(self, image):
        '''function that set image to label and send message to messagebar'''
        if not PyQt5.sip.isdeleted(self.CameraLabel):
            self.CameraLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            if self.cameraManager.prediction:
                self.right_label.setText(self.cameraManager.prediction)
            else:
                self.right_label.setText(self.cameraManager.prompt)

    def setCameraIcon(self):
        self.CameraLabel.setPixmap(PyQt5.QtGui.QPixmap(
            f"{current_directory}/icons/camera.ico"))

    def camera_layout(self):
        CameraWidget = PyQt5.QtWidgets.QWidget(objectName='CameraWidget')
        CameraLayout = PyQt5.QtWidgets.QGridLayout(objectName='CameraLayout')
        self.CameraLabel = PyQt5.QtWidgets.QLabel(objectName='CameraLabel')
        self.setCameraIcon()
        self.CameraLabel.setFixedSize(640, 480)
        self.CameraLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        CameraLayout.setAlignment(PyQt5.QtCore.Qt.AlignLeft)
        CameraLayout.addWidget(self.CameraLabel)
        CameraWidget.setLayout(CameraLayout)
        self.LeftArea.addWidget(CameraWidget)

    def drop_file_layout_single(self):
        text = 'перетащите файл \n или выберите для перевода'
        DropWidget = PyQt5.QtWidgets.QWidget(objectName='DragDrop')
        DropLayout = PyQt5.QtWidgets.QGridLayout(objectName='DragDropLayout')

        self.DropIcon = DragAndDropWidget_single(parent=self, shadow=True)
        self.DropIcon.setPixmap(PyQt5.QtGui.QPixmap(
            f"{current_directory}/icons/drop_file.ico"))
        self.DropIcon.setAlignment(
            PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignTop)
        self.DropIcon.setFixedSize(720, 480)
        self.DropIcon.setObjectName('DropLabel')

        self.DropLabel_single = DragAndDropWidget_single(parent=self)
        self.DropLabel_single.setObjectName('DropLabel')
        self.DropLabel_single.setText(text)
        self.DropLabel_single.setAlignment(
            PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignBottom)

        DropLayout.addWidget(self.DropLabel_single, 0, 0)
        DropLayout.addWidget(self.DropIcon, 0, 0)
        DropWidget.setLayout(DropLayout)
        self.LeftArea.addWidget(DropWidget)

    def drop_file_layout_multi(self):
        text = 'перетащите файл \n или выберите для перевода'
        DropWidget = PyQt5.QtWidgets.QWidget(objectName='DragDrop')
        DropLayout = PyQt5.QtWidgets.QGridLayout(objectName='DragDropLayout')

        self.DropIcon = DragAndDropWidget_Multiple(parent=self, shadow=True)
        self.DropIcon.setPixmap(PyQt5.QtGui.QPixmap(
            f"{current_directory}/icons/drop_file.ico"))
        self.DropIcon.setAlignment(
            PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignTop)
        self.DropIcon.setFixedSize(720, 480)
        self.DropIcon.setObjectName('DropLabel')

        self.DropLabel = DragAndDropWidget_Multiple(parent=self)
        self.DropLabel.setObjectName('DropLabel')
        self.DropLabel.setText(text)
        self.DropLabel.setAlignment(
            PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignBottom)

        DropLayout.addWidget(self.DropLabel, 0, 0)
        DropLayout.addWidget(self.DropIcon, 0, 0)
        DropWidget.setLayout(DropLayout)
        self.LeftArea.addWidget(DropWidget)

    def make_Left_Layout(self):
        'creates main stacked layout which consist other three'
        self.LeftArea = PyQt5.QtWidgets.QStackedLayout(objectName='LeftArea')
        self.LeftArea.setAlignment(
            PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignVCenter)
        self.drop_file_layout_single()
        self.drop_file_layout_multi()
        self.camera_layout()
        self.LeftArea.setAlignment(PyQt5.QtCore.Qt.AlignLeft)
        self.main_layout.addLayout(self.LeftArea, 1, 0, 1, 1)

    def make_Right_layout(self):
        self.right_layout = PyQt5.QtWidgets.QStackedLayout(
            objectName='RightArea')

        self.right_label = PyQt5.QtWidgets.QLabel(
            'Перевод', objectName='RightLabel')
        self.right_label.setFixedSize(720, 480)
        self.right_label.setAlignment(
            PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignVCenter)

        self.right_layout.setAlignment(PyQt5.QtCore.Qt.AlignLeft)
        self.right_layout.addWidget(self.right_label)
        self.main_layout.addLayout(self.right_layout, 1, 1, 1, 1)

    def start_stream(self):
        self.LeftArea.setCurrentIndex(2)
        self.cameraManager.switch_to_stream()

    def get_stream_button(self):
        stream_button = PyQt5.QtWidgets.QPushButton(
            'Прямой эфир', objectName='MenuButton')
        stream_button.setToolTip(
            'Переводит язык жестов в текст в прямом эфире')
        stream_button.clicked.connect(self.start_stream)
        return stream_button

    def mono_button_actions(self):
        self.LeftArea.setCurrentIndex(0)
        self.cameraManager.stop_capturing()

    def get_mono_button(self):
        mono_button = PyQt5.QtWidgets.QPushButton(
            'Однознаковый', objectName='MenuButton')
        mono_button.setToolTip(
            'Обрабатывает видео содержащие в себе не более одного знака РЖЯ')
        mono_button.clicked.connect(self.mono_button_actions)
        return mono_button

    def multi_button_actions(self):
        self.LeftArea.setCurrentIndex(1)
        self.cameraManager.stop_capturing()

    def get_multi_button(self):
        multi_button = PyQt5.QtWidgets.QPushButton(
            'Многознаковый', objectName='MenuButton')
        multi_button.setToolTip(
            'Обрабатывает видео содержащие в себе более одного знака РЖЯ')
        multi_button.clicked.connect(self.multi_button_actions)
        return multi_button

    def create_menu_layout(self):

        menu_layout = PyQt5.QtWidgets.QHBoxLayout(objectName='MenuArea')
        logo_label = PyQt5.QtWidgets.QLabel(
            'Выберите режим перевода:', objectName='LogoLabel')

        stream_button = self.get_stream_button()
        mono_button = self.get_mono_button()
        multi_button = self.get_multi_button()

        menu_layout.addWidget(logo_label)
        menu_layout.addWidget(mono_button)
        menu_layout.addWidget(multi_button)
        menu_layout.addWidget(stream_button)

        self.main_layout.addLayout(menu_layout, 0, 0, 1, 1)
        menu_layout.setAlignment(
            PyQt5.QtCore.Qt.AlignVCenter | PyQt5.QtCore.Qt.AlignLeft)

    def left_history_area(self):
        self.left_history_layout = PyQt5.QtWidgets.QVBoxLayout(
            objectName='HistoryArea')
        self.left_history_layout.setAlignment(
            PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignHCenter)
        tool_label = PyQt5.QtWidgets.QLabel(
            'источник', objectName='HistoryTitleToolLeft')
        self.left_history_layout.addWidget(tool_label)
        self.history_area.addLayout(self.left_history_layout, 1, 0,)

    def right_history_area(self):
        self.right_history_layout = PyQt5.QtWidgets.QVBoxLayout(
            objectName='HistoryArea')
        self.right_history_layout.setAlignment(
            PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignHCenter)
        tool_label = PyQt5.QtWidgets.QLabel(
            'вывод', objectName='HistoryTitleToolRight')
        self.right_history_layout.addWidget(tool_label)
        self.history_area.addLayout(self.right_history_layout, 1, 1)

    def create_history_area(self):

        self.scroll = QtWidgets.QScrollArea(objectName='ScrollArea')
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(200)
        self.scroll_widget = QtWidgets.QWidget(objectName='ScrollWidget')
        self.history_widget = QtWidgets.QWidget(objectName='ScrollWidget')

        vbox = QtWidgets.QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.history_widget)
        vbox.addStretch()

        self.history_area = PyQt5.QtWidgets.QGridLayout()
        self.history_area.setAlignment(
            PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignLeft)
        title_label = PyQt5.QtWidgets.QLabel(
            'История', objectName='HistoryTitle')
        title_label.setAlignment(
            PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignLeft)
        self.history_area.addWidget(title_label, 0, 0, 1, 0)
        self.right_history_area()
        self.left_history_area()
        self.history_widget.setLayout(self.history_area)

        self.scroll.setWidget(self.history_widget)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.scroll)

        self.main_layout.addLayout(layout, 2, 0, 2, 2)

    def create_main_layout(self):
        self.main_layout = PyQt5.QtWidgets.QGridLayout()
        self.main_layout.setAlignment(
            PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignHCenter)
        self.setLayout(self.main_layout)

    def setDefaults(self):
        self.setObjectName('MainWindow')
        self.setWindowTitle("Переводчик с русского языка жестов в текст")
        self.setMaximumSize(1600, 800)

    def CreateGUI(self):
        self.setDefaults()
        self.create_main_layout()
        self.create_menu_layout()
        self.make_Left_Layout()
        self.make_Right_layout()
        self.create_history_area()


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
