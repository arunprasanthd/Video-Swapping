import sys, os
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QMainWindow,
                             QAction, QShortcut, QCheckBox, QGridLayout)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.uic import loadUi


class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('Video Swapping.ui', self)

        self.openButton.clicked.connect(self.openFile)
        self.playButton.clicked.connect(self.playFile)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.frameLayout.addWidget(videoWidget)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))

    def playFile(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setText('Pause')
        else:
            self.mediaPlayer.play()
            self.playButton.setText('Play')


app = QApplication(sys.argv)
mainwindow = VideoWindow()
mainwindow.show()
sys.exit(app.exec_())
