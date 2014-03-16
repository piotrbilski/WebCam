'''
Created on 15-03-2014

@author: piotr
'''
import sys
import numpy
import cv2
import time
from PySide import QtCore, QtGui


class QCamera(QtCore.QThread):
    
    PictureSignal = QtCore.Signal(numpy.ndarray)
    CameraStateSignal = QtCore.Signal(bool)
    
    cap = None
    
    def __init__(self, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.sayCheese = True
        try:
            self.cap = cv2.VideoCapture(0)
            self.CameraStateSignal.emit(True)
        except Exception:
            self.CameraStateSignal.emit(False)
            pass

    def run(self):
        while self.sayCheese:
            self.capturePic()
        self.sayCheese = True

            
    def capturePic(self):
        ret, frame = self.cap.read()
        self.PictureSignal.emit(frame)
        
    def stopThread(self):
        self.sayCheese = False
        
        


class MainWindow(QtGui.QWidget):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__(self, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Webcam Tools")
        
        self.camera = QCamera()
        
        self.camera.PictureSignal.connect(self.displayPic)
        self.camera.CameraStateSignal.connect(self.readyCamera)
        
        hLayout = QtGui.QHBoxLayout()
        self.leftLabel = QtGui.QLabel('Left pic')
        self.rightLabel = QtGui.QLabel('Right pic')
        
        
        hLayout.addWidget(self.leftLabel)
        hLayout.addWidget(self.rightLabel)
        
        vLayout = QtGui.QVBoxLayout()
        vLayout.addLayout(hLayout)
        self.makePic = QtGui.QPushButton("Start")
        self.makePic.clicked.connect(self.capturePic)
        vLayout.addWidget(self.makePic)
        
        
        self.setLayout(vLayout)
        self.setVisible(True)
        
    def __arrayToQPixmap(self, frame):
        picture = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)
        #convert numpy mat to pixmap image
        qimg = QtGui.QImage(picture.data,picture.shape[1], picture.shape[0], QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(qimg)

    def readyCamera(self, status):
        if status:
            self.makePic.setEnabled()
            return
        self.makePic.setDisabled()
            
        
    def displayPic(self, picArray):
        
        self.leftLabel.setPixmap(self.__arrayToQPixmap(picArray))
        self.rightLabel.setPixmap(self.__arrayToQPixmap(picArray))
        
    def capturePic(self):
        if self.camera.isRunning():
            self.camera.stopThread()
        else:
            self.camera.start()
        

if __name__ == '__main__':
    
    Application = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(Application.exec_())