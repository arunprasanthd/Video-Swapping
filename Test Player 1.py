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
        self.mediaPlayers = []
        self.videoWidgets = []
        self.selector = []

        for i in range(4):
            self.mediaPlayers.append(QMediaPlayer(None, QMediaPlayer.VideoSurface))
            self.videoWidgets.append(QVideoWidget())
            self.mediaPlayers[i].setVideoOutput(self.videoWidgets[i])
            self.frameLayout.addWidget(self.videoWidgets[i])

        self.openButton.clicked.connect(self.openFile)
        self.playButton.clicked.connect(self.playFile)

        for i in self.mediaPlayers:
            i.stateChanged.connect(self.mediaStateChanged)

    def openFile(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select up to 4 files", QDir.homePath())
        for m, f in zip(self.mediaPlayers, files):
            m.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
        self.playButton.setEnabled(True)

    def playFile(self):
        for i in self.mediaPlayers:
            if i.state() == QMediaPlayer.PlayingState:
                i.pause()
            else:
                i.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayers[0].state() == QMediaPlayer.PlayingState:
            self.playButton.setText('Pause')
        else:
            self.playButton.setText('Play')


app = QApplication(sys.argv)
mainwindow = VideoWindow()
mainwindow.show()
sys.exit(app.exec_())
