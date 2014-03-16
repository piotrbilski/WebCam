'''
Created on 15-03-2014

@author: piotr
'''
import sys
import numpy
import cv2
from PySide import QtCore, QtGui


class QCamera(QtCore.QObject):
    
    PictureSignal = QtCore.Signal(numpy.ndarray)
    cap = None
    
    def __init__(self, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        self.cap = cv2.VideoCapture(0)

    def capturePic(self):
        ret, frame = self.cap.read()
        self.PictureSignal.emit(frame)
        
        


class MainWindow(QtGui.QWidget):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__(self, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Webcam Tools")
        
        self.camera = QCamera()
        self.camera.PictureSignal.connect(self.displayPic)
        
        hLayout = QtGui.QHBoxLayout()
        self.leftLabel = QtGui.QLabel('Left pic')
        self.rightLabel = QtGui.QLabel('Right pic')
        
        
        hLayout.addWidget(self.leftLabel)
        hLayout.addWidget(self.rightLabel)
        
        vLayout = QtGui.QVBoxLayout()
        vLayout.addLayout(hLayout)
        makePic = QtGui.QPushButton("Make a pic")
        makePic.clicked.connect(self.capturePic)
        vLayout.addWidget(makePic)
        
        
        self.setLayout(vLayout)
        self.setVisible(True)
        
    def __arrayToQPixmap(self, frame):
        picture = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)
        #convert numpy mat to pixmap image
        qimg = QtGui.QImage(picture.data,picture.shape[1], picture.shape[0], QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(qimg)

        
    def displayPic(self, picArray):
        
        self.leftLabel.setPixmap(self.__arrayToQPixmap(picArray))
        self.rightLabel.setPixmap(self.__arrayToQPixmap(picArray))
        
    def capturePic(self):
        self.camera.capturePic()

if __name__ == '__main__':
    
    Application = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(Application.exec_())