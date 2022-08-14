import math
from typing import Type
import onnxruntime
import albumentations as albu
import cv2
import PyQt5
from PyQt5 import QtCore, QtGui
import numpy as np
import os
import time
import sys
import torch

if sys.platform == 'win32':
    current_directory = ''.join(
        [x + '/' for x in os.path.realpath(__file__).split('\\')[:-1]])[:-1]
else:
    current_directory = ''.join(
        [x + '/' for x in os.path.realpath(__file__).split('/')[:-1]])[:-1]

classes = ['A', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', "Й", 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц',
           'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', "мама", 'читать', 'книга', 'бабушка', 'вязать', 'голубой',
           'ресторан', 'стоить', 'дорого', 'плавать', 'река', 'зима', 'такси', 'ребенок', 'прогулка', 'собака', 'лето', 'город']


def softmax(X):
    expo = np.exp(X)
    expo_sum = np.sum(np.exp(X))
    return expo / expo_sum


class CFG:
    '''
    Concfiguration class
    '''
    NUM_FRAMES = 64
    NUM_FRAMES_STREAM = 16
    SIZE = 112
    THRESHOLD = 0.7
    classification_session = onnxruntime.InferenceSession(
        f'{current_directory}/weights/r2+1d_112_64_main.onnx')
    stream_session = onnxruntime.InferenceSession(
        f'{current_directory}/weights/r3d18_112_16.onnx')
    yolo_model = torch.hub.load(
        'ultralytics/yolov5', 'yolov5s', pretrained=True)

    second_transform = albu.Compose([
        albu.Resize(SIZE, SIZE),
        albu.CLAHE(p=1),
        albu.Normalize(mean=[0.43216, 0.394666, 0.37645],
                       std=[0.22803, 0.22145, 0.216989])])


def find_bounding_box(frames):
    results = CFG.yolo_model(frames).xyxy
    x_min, y_min, x_max, y_max = math.inf, math.inf, 0, 0
    for i in range(len(frames)):
        for j in range(len(results[i])):
            if results[i][j][5] == 0:
                if results[i][j][0] < x_min:
                    x_min = results[i][j][0]
                if results[i][j][1] < y_min:
                    y_min = results[i][j][1]
                if results[i][j][2] > x_max:
                    x_max = results[i][j][2]
                if results[i][j][3] > y_max:
                    y_max = results[i][j][3]
    return (int(x_min), int(y_min), int(x_max), int(y_max))


def inf_main_nn(image):
    ort_inputs = {CFG.classification_session.get_inputs()[0].name: image}
    ort_outs = CFG.classification_session.run(None, ort_inputs)
    return ort_outs[0][0]


def inf_stream_nn(image):
    ort_inputs = {CFG.stream_session.get_inputs()[0].name: image}
    ort_outs = CFG.stream_session.run(None, ort_inputs)
    return ort_outs


class MLManager_MonoValued(PyQt5.QtCore.QThread):
    makePrediction = PyQt5.QtCore.pyqtSignal(str)
    PATH = None

    def run(self):
        '''
        main function to inference videos which consists 
        1-single sign per video
        '''
        # Чтение кадров
        frames = []
        cap = cv2.VideoCapture(self.PATH)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
            else:
                break
        cap.release()

        yolo_frames = []
        for i in range(0, len(frames), len(frames) // 5):
            yolo_frames.append(frames[i])

        x_min, y_min, x_max, y_max = find_bounding_box(yolo_frames)

        # Обработка кадров и inference основной сети
        frame_list = []
        part = len(frames) / CFG.NUM_FRAMES
        for i in range(CFG.NUM_FRAMES):
            self.parent.progress_bar.bar.setValue(i + 1)
            frame = frames[int(part * i)][y_min:y_max, x_min:x_max]
            frame_list.append(CFG.second_transform(image=frame)['image'])
        frame_list = np.array([frame_list]).transpose((0, 4, 1, 2, 3))
        pred = softmax(inf_main_nn(frame_list))
        prediction = classes[pred.argmax()]
        prediction = prediction if prediction else ''
        self.makePrediction.emit(prediction)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.terminate()

    def switch_to_MonoValue(self):
        '''activate stream mode'''
        self.makePrediction.connect(self.parent.MonoValuePrediction)
        self.start()


class MLManager_MultiValued(PyQt5.QtCore.QThread):
    makePrediction = PyQt5.QtCore.pyqtSignal(list)
    PATH = None
    # Главная функция для multiple

    def run(self):
        # Обработка видео
        frames = []
        cap = cv2.VideoCapture(self.PATH)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
            else:
                break
        cap.release()

        if len(frames) < CFG.NUM_FRAMES:
            tmp_frames = frames
            part = len(frames) / CFG.NUM_FRAMES
            frames = []
            for i in range(CFG.NUM_FRAMES):
                frames.append(tmp_frames[int(part*i)])

        yolo_frames = []
        for i in range(0, len(frames), len(frames) // 5):
            yolo_frames.append(frames[i])

        x_min, y_min, x_max, y_max = find_bounding_box(yolo_frames)

        indexes = range(0, len(frames) - CFG.NUM_FRAMES +
                        1, CFG.NUM_FRAMES // 2)

        # Inference основной сети сквозным окном
        prediction = []
        duration = []

        self.parent.progress_bar.bar.setRange(0, max(max(list(indexes)), 1))
        for i in indexes:
            self.parent.progress_bar.bar.setValue(i + 1)
            pred_frames = frames[i:i+CFG.NUM_FRAMES]
            pred_frames = [CFG.second_transform(image=fr[y_min:y_max, x_min:x_max])[
                'image'] for fr in pred_frames]
            pred_frames = np.array([pred_frames]).transpose((0, 4, 1, 2, 3))
            pred = softmax(inf_main_nn(pred_frames))
            if pred.max() > 0.5 and (not prediction or prediction[-1] != pred.argmax()):
                prediction.append(pred.argmax())
                duration.append((i, i+CFG.NUM_FRAMES))

        prediction = [f'{classes[x]}' for x in prediction]
        time_series = dict(zip(prediction, duration))
        prediction = [f'{pred}, ' for pred in prediction]

        prediction = ''.join(prediction)[:-2] if prediction else ''
        print(time_series)

        self.makePrediction.emit([prediction, time_series])

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.terminate()

    def switch_to_MonoValue(self):
        '''activate stream mode'''
        self.makePrediction.connect(self.parent.MonoValuePrediction)
        self.start()


class MLManager_Stream(PyQt5.QtCore.QThread):
    makePrediction = PyQt5.QtCore.pyqtSignal()
    frames = list()

    def run(self):  # Основная функция стрима
        # preprocessing frames
        part = len(self.frames) / CFG.NUM_FRAMES_STREAM
        need_frames = [self.frames[int(part * i)]
                       for i in range(CFG.NUM_FRAMES_STREAM)]
        # Inference U-net

        yolo_frames = []
        for i in range(0, len(need_frames), len(need_frames) // 3):
            yolo_frames.append(need_frames[i])

        x_min, y_min, x_max, y_max = find_bounding_box(yolo_frames)
        # print(x_min, y_min, x_max, y_max)

        if x_max == 0:
            return False

        # Inference of the main network
        new_frames = []
        cv2.imwrite('frame_tmp.jpg', need_frames[0][y_min:y_max, x_min:x_max])
        for i, frame in enumerate(need_frames):
            frame = frame[y_min:y_max, x_min:x_max]
            new_frames.append(CFG.second_transform(image=frame)['image'])
        new_frames = np.array([new_frames]).transpose((0, 4, 1, 2, 3))
        pred = softmax(inf_stream_nn(new_frames))
        # print(pred)
        prediction = classes[pred.argmax()] if pred.max(
        ) > CFG.THRESHOLD else ''
        print(f'{pred.max()} : {classes[pred.argmax()]}\n')
        if not prediction:
            prediction = ''
        self.parent.prediction = prediction
        if prediction:
            self.parent.history += f'{prediction}, '
        # self.makePrediction.emit(prediction)
        self.makePrediction.emit()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        # self._run_flag = False
        # self.terminate()
        pass

    # def switchToStream(self):
        # '''activate stream mode'''
        # self.makePrediction.connect(self.parent.get_prediction)
        # self.start()
