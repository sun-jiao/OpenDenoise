from PySide6.QtCore import Qt
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


def openUrl(url: str):
    url = QUrl(url)
    QDesktopServices.openUrl(url)
