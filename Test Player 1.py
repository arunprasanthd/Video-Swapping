import sys, os
from PyQt5.QtCore import QDir, Qt, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QMainWindow,
                             QAction, QShortcut, QCheckBox, QGridLayout)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.uic import loadUi


class QVideoClickableWidget(QVideoWidget):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QVideoClickableWidget, self).__init__(parent)

    def mousePressEvent(self, event):
        self.ultimo = "Clic"

    def mouseReleaseEvent(self, event):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)

    def performSingleClickAction(self):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)


class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('Video Swapping.ui', self)
        self.mediaPlayers = []
        self.videoWidgets = []
        self.selector = []

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.gLay.addWidget(videoWidget)


        for i in range(4):
            self.mediaPlayers.append(QMediaPlayer(None, QMediaPlayer.VideoSurface))
            self.videoWidgets.append(QVideoClickableWidget())
            self.mediaPlayers[i].setVideoOutput(self.videoWidgets[i])
            self.vLayout.addWidget(self.videoWidgets[i])

        self.openButton.clicked.connect(self.openFile)
        self.playButton.clicked.connect(self.playFile)

        # for i in self.videoWidgets:
            # i.clicked.connect(self.clickAction)

        for c, d in zip(self.videoWidgets, self.videoWidgets):
            c.clicked.connect(lambda xy, d=d: self.clickAction(self.videoWidgets.index(d)))

        for i in self.mediaPlayers:
            i.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)


    def openFile(self):
        self.files, _ = QFileDialog.getOpenFileNames(self, "Select up to 4 files", QDir.homePath())
        self.clickedFileNumber = 0
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.files[self.clickedFileNumber])))
        for m, f in zip(self.mediaPlayers, self.files):
            m.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
        self.playButton.setEnabled(True)

    def clickAction(self, a):
        # self.clickedFileNumber = a
        # self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.files[self.clickedFileNumber])))
        print(a)
        


    def playFile(self):
        for i in self.mediaPlayers:
            if i.state() == QMediaPlayer.PlayingState :
                i.pause()
                self.mediaPlayer.pause()
            else:
                i.play()
                self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayers[0].state() == QMediaPlayer.PlayingState:
            self.playButton.setText('Pause')
        else:
            self.playButton.setText('Play')


app = QApplication(sys.argv)
mainwindow = VideoWindow()
mainwindow.show()
sys.exit(app.exec_())
