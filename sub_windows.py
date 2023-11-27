from PySide6.QtCore import Qt
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from utils import openUrl


class NotImplementedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        label_0 = QLabel('This feature is still in progress. ')
        label = QLabel(self)
        label.setText('It may appears in new '
                      '<a href="https://github.com/sun-jiao/OpenDenoise/releases">releases</a>.')
        label.setOpenExternalLinks(True)
        label.linkActivated.connect(openUrl)

        layout = QVBoxLayout()
        layout.addWidget(label_0)
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle('Not Implemented!')
        self.show()


class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        label_0 = QLabel('Open Denoise is an application for denoising photos using deep learning.')
        label = QLabel(self)
        label.setText('It is powered by <a href="https://github.com/cszn/SCUNet">Swin-Conv-UNet model</a> '
                      'that proposed by <a href="https://link.springer.com/article/10.1007/s11633-023-1466-0">Zhang Kai <i>et al</i></a>.')
        label.setOpenExternalLinks(True)
        label.linkActivated.connect(openUrl)

        label_1 = QLabel('This app is released under GPLv3. <br>SCUNet is released under Apache 2.0.')

        layout = QVBoxLayout()
        layout.addWidget(label_0)
        layout.addWidget(label)
        layout.addWidget(label_1)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Align buttons to the top

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle('About the app')
        self.show()
