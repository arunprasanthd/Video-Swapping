import sys
import os
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
        # self.selector = []

        self.openButton.clicked.connect(self.openFile)
        self.playButton.clicked.connect(self.playFile)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoClickableWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.gLay.addWidget(self.videoWidget)

        for i in range(4):
            self.mediaPlayers.append(QMediaPlayer(None, QMediaPlayer.VideoSurface))
            self.videoWidgets.append(QVideoClickableWidget())
            self.mediaPlayers[i].setVideoOutput(self.videoWidgets[i])
            self.vLayout.addWidget(self.videoWidgets[i])

        # for c, d in zip(self.videoWidgets, self.files):
        #     c.clicked.connect(lambda xy, d=d: self.clickAction(d))

    def openFile(self):
        # fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        self.files, _ = QFileDialog.getOpenFileNames(self, 'Select up to 4 files', QDir.homePath())
        self.fileName = self.files[0]

        for c, d in zip(self.videoWidgets, self.files):
            c.clicked.connect(lambda xy, d=d: self.clickAction(d))

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
        for m, f in zip(self.mediaPlayers, self.files):
            m.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
            self.playButton.setEnabled(True)


    def playFile(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState and self.mediaPlayers[0].state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            for i in self.mediaPlayers:
                i.pause()
            self.playButton.setText('Pause')
        else:
            self.mediaPlayer.play()
            for i in self.mediaPlayers:
                i.play()
            self.playButton.setText('Play')

    def clickAction(self, a):
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile(a)))


app = QApplication(sys.argv)
mainwindow = VideoWindow()
mainwindow.show()
sys.exit(app.exec_())
